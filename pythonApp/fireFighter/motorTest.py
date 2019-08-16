import serial
import communicationHandler
import motorController
from time import sleep

serialLink = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialLink)

motors = motorController.MotorController(commHandler)

while True:
    motors.turn(45.0, 255)
    sleep(1)


