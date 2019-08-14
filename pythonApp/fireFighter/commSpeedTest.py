import communicationHandler
import serial
import motorController
import time

serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorHandler(commHandler)

tStart = time.time()
commHandler.get_light_sensors_data()
tEnd = time.time()

print((tEnd - tStart) * 1000)