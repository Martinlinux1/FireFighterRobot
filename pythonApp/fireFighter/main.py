import serial
import communicationHandler
import motorController
from pyusb2fir import USB2FIR
from time import sleep

serialLink = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialLink)

motors = motorController.MotorHandler(commHandler)

base_speed = 255

value_black = 500

thermal_camera = USB2FIR()

sleep(2)

while True:
    temperatures_raw_0 = thermal_camera.initializeFrame()
    temperatures_raw_1 = thermal_camera.initializeFrame()
    temperatures_raw = []

    thermal_camera.updateFrame(temperatures_raw_0)
    thermal_camera.updateFrame(temperatures_raw_1)

    for i in range(768):
        temperatures_raw.append(temperatures_raw_0[i] + temperatures_raw_1[i])

    index = 0
    temps_row = []
    temps = []
    for i in range(24):
        for j in range(32):
            temps_row.append(temperatures_raw[index])
            index += 1
        temps.append(temps_row)

    for i in range(24):
        for j in range(32):
            if temps[i][j] > 50:
                print("Fire on(x, y): ", (j, i))

                angle_x = i * (120 / 32) - 60
                angle_y = j * (75 / 24) - 37.5

                if angle_x < 0:
                    while angle_x < -5:
                        motors.turn(direction='L', speed=base_speed)
                elif angle_x > 0:
                    while angle_x > 5:
                        motors.turn(direction='L', speed=base_speed)

                motors.brake()

                while commHandler.get_light_sensor_data(0) > value_black:
                    motors.forward('AB', base_speed)
                motors.brake()

