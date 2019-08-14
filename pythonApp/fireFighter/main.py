import threading
import serial
from time import sleep

import RPi.GPIO as GPIO
from gpiozero import Servo

from pyusb2fir import USB2FIR
from cameraReader import CameraReader

import motorController
import communicationHandler
from MathUtils import MathUtils


def camera_fetcher():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        x = cam.read_camera()


fanPin = 4

servo = Servo(14)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(fanPin, GPIO.OUT)
GPIO.output(fanPin, GPIO.HIGH)

thermal_camera = USB2FIR()
# serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
t = threading.Thread(target=camera_fetcher)
t.daemon = True

cam = CameraReader(thermal_camera)
# commHandler = communicationHandler.CommunicationHandler(serialPort)
# motors = motorController.MotorHandler(commHandler)

baseSpeed = 150

t.start()


print("camera testing", end="")
while cam.read_camera()[0] == 0:
    print(".", end="")
    sleep(0.5)

print("\nCamera connected.")
sleep(5)
print("Test completed.")

while True:
    fire_coordinates = cam.is_fire(40)
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

        servo_turn = MathUtils.valmap(max_fire_angle[1], -36, 36, -1, 1)

        servo.value = servo_turn
        GPIO.output(fanPin, GPIO.LOW)
        sleep(5)
        GPIO.output(fanPin, GPIO.HIGH)

    sleep(0.5)
