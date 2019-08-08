import communicationHandler
import serial
import motorController
from time import sleep
import MathUtils

serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorHandler(commHandler)

sleep(10)

while True:
    motors.forward(255)
    sleep(1)
    motors.backward(255)
    sleep(1)
    motors.slide(45, 255)
    sleep(1)
    motors.slide(-135, 255)
    sleep(1)
    motors.slide(90, 255)
    sleep(1)
    motors.slide(-90, 255)
    sleep(1)
    motors.slide(-45, 255)
    sleep(1)
    motors.slide(135, 255)
    sleep(1)



