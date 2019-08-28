import serial
import threading
from time import sleep

from gpiozero import DigitalOutputDevice
from gpiozero import Servo

from pyusb2fir import USB2FIR
from cameraReader import CameraReader

import communicationHandler
import motorController
from MathUtils import MathUtils


# Camera reader
def camera_fetcher():
    thread = threading.currentThread()
    while getattr(thread, "do_run", True):
        cam.read_camera()


turned = False
fanPin = 4

fan = DigitalOutputDevice(fanPin, False)
servo = Servo(14)

thermal_camera = USB2FIR()
serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)
t = threading.Thread(target=camera_fetcher)
t.daemon = True

cam = CameraReader(thermal_camera)
commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorController(commHandler)

baseSpeed = 100

t.start()


print('camera testing', end='')

if thermal_camera.echo_test(44) != 44:
    while True:
        pass
print(thermal_camera.echo_test(5))
print("\nCamera connected.")
sleep(5)
print("Test completed.")
print(cam.read_camera())

while True:
    fire_coordinates = cam.is_fire(40)
    print("v")
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

        if not turned:
            motors.turn(max_fire_angle[0] * -1, baseSpeed)
            turned = True
        else:
            if max_fire_angle in range(-10, 10):
                motors.slide(max_fire_angle[0] * -1, baseSpeed)
            else:
                motors.forward(baseSpeed)

        if max_val[2] > 100:
            motors.brake()
            servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)

            servo.value = servo_angle
            fan.on()
            sleep(5)
            fan.off()
            
            turned = False
