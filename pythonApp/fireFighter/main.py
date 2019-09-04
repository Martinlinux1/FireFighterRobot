import random

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

        # frame = thermal_camera.initializeFrame()
        # ir = frame.reshape((24, 32))
        #
        # matplotlib.use("GTK3Agg")
        # plt.ion()
        # self._graph = plt.imshow(ir, interpolation='none')
        # plt.colorbar()
        # plt.clim(0, 100)
        # plt.draw()
        # plt.show()

    def run(self):
        while self.is_alive():
            ir = cam.read_camera()

            if 0 in ir:
                print("camera reading failure")
            else:
                # ir = np.reshape(ir, (24, 32))
                # self._graph.set_data(ir)
                # plt.draw()
                # plt.pause(0.00001)
                print("camera reading successful")
                camera_data_read_event.set()


def is_line():
    sensors_on_line = []
    for i in range(8):
        if commHandler.get_light_sensor_data(i) > lightSensorsBlack:
            sensors_on_line.append(i)

    return sensors_on_line


camera_data_read_event = threading.Event()

turned = False
fanPin = 4

fan = DigitalOutputDevice(fanPin, False)
servo = Servo(14)

thermal_camera = USB2FIR(refreshRate=5)
serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)

t = CameraFetcher()
t.daemon = True

cam = CameraReader(thermal_camera)
commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorController(commHandler)

baseSpeed = 150

lightSensorsBlack = 600
lightSensorsWhite = 300

t.start()

while True:
    try:
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

            if max_fire_angle[0] > 30 or max_fire_angle[0] < -30:
                if max_fire_angle[0] > 0:
                    motors.turn('L', baseSpeed)
                else:
                    motors.turn('R', baseSpeed)
            else:
                pass
                motors.slide(max_fire_angle[0] * -1, baseSpeed)
            sensors_on_line = is_line()
            if max_fire_angle[0] < 15 and 0 in sensors_on_line:
                print("Extinguishing")
                motors.brake()
                servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)

                servo.value = servo_angle
                fan.on()
                sleep(5)
                fan.off()

                turned = False
        else:
            line = is_line()
            if line:
                if 6 in line and 5 in line and 4 in line:                   # Left downer corner.
                    motors.turn(45, baseSpeed)
                    motors.forward(baseSpeed)
                elif 2 in line and 3 in line and 4 in line:                 # Right downer corner.
                    motors.turn(-45, baseSpeed)
                elif 0 in line and 7 in line and 6 in line:                 # Left upper corner.
                    motors.turn(135, baseSpeed)
                elif 0 in line and 1 in line and 2 in line:                 # Right upper corner.
                    motors.turn(-135, baseSpeed)
                elif 6 in line and (7 in line or 5 in line):                # Line on the left.
                    motors.turn(90, baseSpeed)
                elif 0 in line and (7 in line or 1 in line):                # Line on the right.
                    motors.turn(-90, baseSpeed)
                elif 4 in line and (5 in line or 3 in line):                # Line on the back.
                    motors.turn(180, baseSpeed)
                elif 2 in line and (1 in line or 3 in line):                # Line on the front.
                    motors.turn(180, baseSpeed)
                else:                                                       # One sensor detected the line.
                    if 1 in line:
                        motors.backward(baseSpeed)
                        sleep(0.1)
                        motors.turn(random.randint(-45, -75), baseSpeed)
                    elif 3 in line:
                        motors.forward(baseSpeed)
                        sleep(0.1)
                        motors.turn(random.randint(-45, -75), baseSpeed)
                    elif 5 in line:
                        motors.forward(baseSpeed)
                        sleep(0.1)
                        motors.turn(random.randint(45, 75), baseSpeed)
                    elif 7 in line:
                        motors.backward(baseSpeed)
                        sleep(0.1)
                        motors.turn(random.randint(45, 75), baseSpeed)
            else:
                motors.forward(baseSpeed)

    except KeyboardInterrupt:
        print('Exiting program.')
        break
