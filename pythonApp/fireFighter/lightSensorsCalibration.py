import serial
from time import sleep

from IO import commiface

serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)
commHandler = commiface.CommInterface(serialPort)


print("Put your robot on white color, and press any key.")
input()
print("White color calibrating...")

white_value = 0
for i in range(200):
    sensor_value = commHandler.get_light_sensor_data(0)
    if sensor_value > white_value:
        white_value = sensor_value
    sleep(0.01)

print("Done.")

print("Put your robot on black color, and press any key.")
input()
print("Black color calibrating...")

black_value = 10000
for i in range(200):
    sensor_value = commHandler.get_light_sensor_data(0)
    if sensor_value < black_value:
        black_value = sensor_value
    sleep(0.01)

print("Done.")

print("White value: ", white_value)
print("Black color value: ", black_value)