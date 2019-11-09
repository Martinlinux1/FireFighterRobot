import multiprocessing
from time import sleep

# from gpiozero import DigitalOutputDevice
import serial

import communication
import communicationHandler

import motorsWriter
import sensorsReader

import motorController


def robot_data_handler(comm_child_pipe):
    c = comm_child_pipe.recv()
    while True:
        c.update_sensors()
        comm_child_pipe.send(c)
        # print(t_end - t_start
        c = comm_child_pipe.recv()
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


def turn(angle, speed, c):
    if comm_parent.poll():
        c = comm_parent.recv()

    robot_angle = c.get_imu_sensor()
    target_angle = robot_angle + angle
    target_angle = target_angle % 360

    if target_angle < 0:
        target_angle = target_angle + 360

    while True:
        if comm_parent.poll():
            c = comm_parent.recv()

        m = motorController.MotorController(c, 0.05)
        robot_angle = c.get_imu_sensor()

        print(robot_angle)

        diff = target_angle - robot_angle
        direction = 180 - (diff + 360) % 360

        if direction > 0:
            m.right(speed)
        else:
            m.left(speed)
        comm_parent.send(c)

        if abs(diff) < 5:
            m.brake()
            comm_parent.send(c)
            return


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
comm_handler = communicationHandler.CommunicationHandler(serial_port)

sensors_reader = sensorsReader.SensorsReader(comm_handler)
motors_writer = motorsWriter.MotorsWriter(comm_handler)

comm: communication.Communication = communication.Communication(comm_handler, sensors_reader, motors_writer)

motors = motorController.MotorController(comm, 0.05)

comm_parent, comm_child = multiprocessing.Pipe()

robot_logic_process = multiprocessing.Process(target=robot_data_handler, args=[comm_child])
comm_parent.send(comm)

robot_logic_process.start()

base_speed = 100

while not comm_parent.poll():
    pass

while True:
    comm = comm_parent.recv()

    motors = motorController.MotorController(comm, 0.05)

    light_sensors = comm.get_light_sensors()
    distance_sensors = comm.get_distance_sensors()
    imu_sensor = comm.get_imu_sensor()

    sensors_on_line = is_line(light_sensors)
    obstacles = is_obstacle(distance_sensors)

    print(sensors_on_line)
    print(obstacles)

    if sensors_on_line:
        if (0 or 7) in sensors_on_line:
            motors.backward(base_speed)
            comm_parent.send(comm)
            sleep(0.1)
            turn(60, base_speed, comm)
        elif 1 in sensors_on_line:
            motors.backward(base_speed)
            comm_parent.send(comm)
            sleep(0.1)
            turn(-60, base_speed, comm)

    # if 0 in obstacles:
    #     turn(-90, base_speed)
    # elif 1 in obstacles:
    #     turn(-45, base_speed)
    # elif 3 in obstacles:
    #     turn(45, base_speed)

    else:
        motors.forward(base_speed)

    comm_parent.send(comm)

    del motors
