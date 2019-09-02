import serial
import threading
from time import sleep
import numpy as np

import matplotlib

import matplotlib.pyplot as plt

from gpiozero import DigitalOutputDevice
from gpiozero import Servo

from pyusb2fir import USB2FIR
from cameraReader import CameraReader

import communicationHandler
import motorController
from MathUtils import MathUtils


# Camera reader
class CameraFetcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        frame = thermal_camera.initializeFrame()
        ir = frame.reshape((24, 32))

        matplotlib.use("GTK3Agg")
        plt.ion()
        self._graph = plt.imshow(ir, interpolation='none')
        plt.colorbar()
        plt.clim(0, 100)
        plt.draw()
        plt.show()

    def run(self):
        while self.is_alive():
            ir = cam.read_camera()

            ir = np.reshape(ir, (24, 32))
            self._graph.set_data(ir)
            plt.draw()
            plt.pause(0.00001)
            print("camera reading successful")
            camera_data_read_event.set()


camera_data_read_event = threading.Event()

turned = False
fanPin = 4

# fan = DigitalOutputDevice(fanPin, False)
# servo = Servo(14)

thermal_camera = USB2FIR()
# serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

t = CameraFetcher()
t.daemon = True

cam = CameraReader(thermal_camera)
# commHandler = communicationHandler.CommunicationHandler(serialPort)
# motors = motorController.MotorController(commHandler)

baseSpeed = 255

t.start()


print('camera testing', end='')

if thermal_camera.echo_test(44) != 44:
    while True:
        pass

print("\nCamera connected.")
sleep(5)
print("Test completed.")
print(cam.read_camera())

while True:
    camera_data_read_event.wait()
    fire_coordinates = cam.is_fire(40)
    camera_data_read_event.clear()

    if fire_coordinates[0]:
        print("Fire on: ", fire_coordinates)

        all_fire_angles = cam.coordinates_to_angle(fire_coordinates[1])

        print("Robot needs to turn: ", all_fire_angles)

        max_val = [0, 0, 0]
        for i in fire_coordinates[1]:
            if i[2] > max_val[2]:
                max_val = i

        print("Fire closest to robot: ", max_val)
        max_fire_angle = CameraReader.coordinates_to_angle(fire_coordinates)

        print("Robot turning: ", max_fire_angle)

        # if max_fire_angle[0] > 20 or max_fire_angle[0] < -20:
        #     if max_fire_angle[0] > 0:
        #         motors.turn('L', baseSpeed)
        #     else:
        #         motors.turn('R', baseSpeed)
        # else:
        #     pass
        #     motors.slide(max_fire_angle[0], baseSpeed)

        if max_val[2] > 100:
            # motors.brake()
            servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)

            # servo.value = servo_angle
            # fan.on()
            # sleep(5)
            # fan.off()
            
            turned = False
    # else:
    #     motors.forward(baseSpeed)

