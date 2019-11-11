import multiprocessing

# from gpiozero import DigitalOutputDevice
import serial

import communicationHandler
import hardwarehandler
import motorController
import motorsWriter
import sensorsReader


def robot_data_handler(c):
    while True:
        print('alive')
        c.update_sensors()
        # print('sensors sent')
        c.update_motors()


def is_line(line_sensors_data):
    on_line_sensors = []
    for i in range(8):
        if line_sensors_data[i] > 2500:
            on_line_sensors.append(i)

    return on_line_sensors


def is_obstacle(distance_sensors_data):
    sensors_detected = []

    for i in range(5):
        if not distance_sensors_data[i]:
            sensors_detected.append(i)

    return sensors_detected


def turn(angle, speed, init_angle):
    robot_angle = init_angle

    target_angle = robot_angle + angle
    target_angle = target_angle % 360

    if target_angle < 0:
        target_angle = target_angle + 360

    while True:
        print('turning')
        sensors_data = hardware_handler.get_sensors()
        robot_angle = sensors_data[2]

        print(robot_angle)

        diff = target_angle - robot_angle
        direction = 180 - (diff + 360) % 360

        if direction > 0:
            motors.right(speed)
        else:
            motors.left(speed)

        if abs(diff) < 5:
            motors.brake()
            return


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
sensors_reader = sensorsReader.SensorsReader(comm_handler)
motors_writer = motorsWriter.MotorsWriter(comm_handler)
hardware_handler: hardwarehandler.HardwareHandler = hardwarehandler.HardwareHandler(sensors_reader, motors_writer)

motors = motorController.MotorController(hardware_handler, 0.05)

robot_logic_process = multiprocessing.Process(target=robot_data_handler, args=[hardware_handler])
robot_logic_process.daemon = True
robot_logic_process.start()

base_speed = 100

while True:
    sensors = hardware_handler.get_sensors()
    try:
        light_sensors = sensors[0]
        distance_sensors = sensors[1]
        imu_sensor = sensors[2]
    except TypeError:
        continue

    sensors_on_line = is_line(light_sensors)
    obstacles = is_obstacle(distance_sensors)

    print(sensors_on_line)
    print(obstacles)

    # if (0 or 7) in sensors_on_line:
    #     motors.backward(base_speed)
    #     sleep(0.1)
    #     turn(60, base_speed, imu_sensor)
    # elif 1 in sensors_on_line:
    #     motors.backward(base_speed)
    #     sleep(0.1)
    #     turn(-60, base_speed, imu_sensor)
    # elif 0 in obstacles:
    #     turn(-90, base_speed, imu_sensor)
    # elif 1 in obstacles:
    #     turn(-45, base_speed, imu_sensor)
    # elif 3 in obstacles:
    #     turn(45, base_speed, imu_sensor)
    #
    # else:
    motors.forward(base_speed)
