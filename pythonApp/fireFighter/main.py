import communicationHandler
import serial
import motorController
from time import sleep


serialPort = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorHandler(commHandler)

baseSpeed = 150
blackThreshold = 500

sleep(5)

while True:
    light_sensors_data = commHandler.get_light_sensors_data()

    i = 0
    for sensor_data in light_sensors_data:
        if sensor_data > blackThreshold:
            if i <= 1:
                motors.backward(baseSpeed)
                sleep(0.1)
                motors.slide(90, baseSpeed)
            elif i == 2:
                motors.slide(-45, baseSpeed)
                motors.slide(90, baseSpeed)
            elif i <= 4:
                motors.slide(90, baseSpeed)
                motors.slide(45, baseSpeed)
            elif i <= 6:
                motors.slide(-45, baseSpeed)
                motors.forward(baseSpeed)
            elif i == 7:
                motors.slide(-135, baseSpeed)
                motors.backward(baseSpeed)
