import serial

from IO import commiface
import motorController


def is_obstacle():
    sensors_detected = []

    for i in range(5):
        distance_data = commHandler.get_distance_sensor_data(i)
        if not distance_data:
            sensors_detected.append(i)

    return sensors_detected


serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.1)

commHandler = commiface.CommInterface(serialPort)
motors = motorController.MotorController(commHandler)

baseSpeed = 150


while True:
    try:
        obstacles = is_obstacle()
        if 0 in obstacles:
            if 2 in obstacles:
                motors.turn(-90, baseSpeed)
            elif 4 in obstacles:
                motors.turn(90, baseSpeed)
            else:
                motors.turn(-90, baseSpeed)
        elif 1 in obstacles:
            motors.turn(-45, baseSpeed)
        elif 3 in obstacles:
            motors.turn(45, baseSpeed)
        else:
            motors.forward(baseSpeed)

    except KeyboardInterrupt:
        print('Exiting program.')
        break

