from IO import commiface
import serial
import motorController
import time

serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

commHandler = commiface.CommInterface(serialPort)
motors = motorController.MotorController(commHandler)

tStart = time.time()
commHandler.get_light_sensors_data()
tEnd = time.time()

print((tEnd - tStart) * 1000)