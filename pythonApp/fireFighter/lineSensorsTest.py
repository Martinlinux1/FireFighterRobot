import threading
from time import sleep

import serial

from IO import commiface
from motors import motors_controller


# from gpiozero import DigitalOutputDevice


class LightSensorReader(threading.Thread):
    def run(self):
        while True:
            print("Reading thread")
            light_data = commHandler.get_light_sensors_data()
            for i in range(8):
                if light_data[i] > lightSensorsBlack:
                    sensors_on_line.append(i)

turned = False
fanPin = 4
sensors_on_line = []

serialPort = serial.Serial("/dev/ttyUSB1", 115200)

commHandler = commiface.CommInterface(serialPort)
motors = motors_controller.MotorController(commHandler, 0.05)           # Adjust the brake delay for your motor.
# onLineLED = DigitalOutputDevice(15)

t1 = LightSensorReader()
lightSensorsReadEvent = threading.Event()
t1.daemon = True

baseSpeed = 100

lightSensorsBlack = 300

previousLine = []
print('Light sensors calibration in 2 seconds...')
sleep(2)
print('calibrating light sensors...')
commHandler.calibrate_light_sensors()
print('DONE.')

t1.start()

while True:
    lock.acquire()
    line = sensors_on_line

    print("Action thread.")

    # if line:
    #     onLineLED.on()

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
    # onLineLED.off()
    lock.release()

t1.join()
print("Ending")
