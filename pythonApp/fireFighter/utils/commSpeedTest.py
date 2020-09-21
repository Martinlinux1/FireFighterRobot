from IO import commiface
import serial
from motors import motors_controller
import time

serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

commHandler = commiface.CommInterface(serialPort)
motors = motors_controller.MotorController(commHandler)

tStart = time.time()
commHandler.get_light_sensors_data()
tEnd = time.time()

print((tEnd - tStart) * 1000)