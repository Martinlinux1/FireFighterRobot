import serial
import communicationHandler
import motorController
from time import sleep

serialLink = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialLink)

motors = motorController.MotorController(commHandler)

while True:
    commHandler.write_motor('A', 'F', 255)
    commHandler.write_motor('B', 'F', 255)
    commHandler.write_motor('C', 'F', 127)
    commHandler.write_motor('D', 'B', 127)

    sleep(5)

    commHandler.write_motor('A', 'B', 255)
    commHandler.write_motor('B', 'B', 255)
    commHandler.write_motor('C', 'B', 127)
    commHandler.write_motor('D', 'F', 127)

    sleep(5)

    commHandler.write_motor('A', 'B', 0)
    commHandler.write_motor('B', 'B', 0)
    commHandler.write_motor('C', 'B', 0)
    commHandler.write_motor('D', 'B', 0)

    commHandler.write_motor('C', 'F', 255)
    commHandler.write_motor('D', 'F', 255)
    commHandler.write_motor('A', 'F', 127)
    commHandler.write_motor('B', 'B', 127)

    sleep(5)

    commHandler.write_motor('C', 'B', 255)
    commHandler.write_motor('D', 'B', 255)
    commHandler.write_motor('A', 'B', 127)
    commHandler.write_motor('B', 'F', 127)

    sleep(5)

    commHandler.write_motor('C', 'B', 0)
    commHandler.write_motor('D', 'B', 0)
    commHandler.write_motor('A', 'B', 0)
    commHandler.write_motor('B', 'B', 0)
