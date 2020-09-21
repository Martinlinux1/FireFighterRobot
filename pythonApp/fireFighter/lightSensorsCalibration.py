import serial
from time import sleep

from IO import commiface
from handlers import sensors_handler

serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
commIface = commiface.CommInterface(serialPort)
sensors = sensors_handler.SensorsHandler(commIface)


print("Put your robot on white color, and press any key.")
input()
print("White color calibrating...")

white_value = 0
for i in range(200):
    light_sensors_value = sensors.get()[0]
    if light_sensors_value[0] > white_value:
        white_value = light_sensors_value[0]
    sleep(0.01)

print("Done.")

print("Put your robot on black color, and press any key.")
input()
print("Black color calibrating...")

black_value = 10000
for i in range(200):
    light_sensors_value = sensors.get()[0]
    if light_sensors_value[0] < white_value:
        black_value = light_sensors_value[0]
    sleep(0.01)

print("Done.")

print("White value: ", white_value)
print("Black color value: ", black_value)
