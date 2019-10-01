import threading
from time import sleep

import serial
import communicationHandler
import motorController


def is_line():
    on_line_sensors = []
    for i in range(8):
        light_data = commHandler.get_light_sensor_data(i)
        if light_data > lightSensorsBlack:
            on_line_sensors.append(i)

    return on_line_sensors


camera_data_read_event = threading.Event()

turned = False
fanPin = 4

serialPort = serial.Serial("/dev/ttyUSB0", 115200)

commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorController(commHandler, 0.05)           # Adjust the brake delay for your motor.

baseSpeed = 150

lightSensorsBlack = 300

previousLine = []
print('Light sensors calibration in 2 seconds...')
sleep(2)
print('calibrating light sensors...')
commHandler.calibrate_light_sensors()
print('DONE.')

while True:
    line = is_line()

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

    if 1 in line:
        motors.backward(baseSpeed)
        sleep(0.3)
        motors.brake()
        print('left')
        motors.turn(-60.0, baseSpeed)
    elif 0 or 7 in line:
        motors.backward(baseSpeed)
        sleep(0.3)
        motors.brake()
        print('right')
        motors.turn(60.0, baseSpeed)
    elif 3 or 5 in line:
        motors.forward(baseSpeed)
        sleep(0.2)