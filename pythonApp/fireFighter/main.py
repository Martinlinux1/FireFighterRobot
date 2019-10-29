import multiprocessing
from time import sleep

import serial

import communication
import communicationHandler
import motorController


def robot_data_handler(comm_child_pipe):
    c: communication.Communication = comm_child_pipe.recv()
    while True:
        c.update_sensors()
        comm_child_pipe.send(c)

        if comm_child_pipe.poll():
            c = comm_child_pipe.recv()
            c.update_motors()


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
comm: communication.Communication = communication.Communication(comm_handler)

motors = motorController.MotorController(comm, 0.05)

comm_parent, comm_child = multiprocessing.Pipe()

robot_logic_process = multiprocessing.Process(target=robot_data_handler, args=[comm_child])
comm_parent.send(comm)

robot_logic_process.start()

base_speed = 150


def is_line(line_sensors_data):
    on_line_sensors = []
    for i in range(8):
        if line_sensors_data[i] > 2000:
            on_line_sensors.append(i)

    return on_line_sensors


def is_obstacle(distance_sensors_data):
    sensors_detected = []

    for i in range(5):
        if not distance_sensors_data[i]:
            sensors_detected.append(i)

    return sensors_detected


def turn(angle, speed):
    comm = comm_parent.recv()
    robot_angle = comm.get_imu_sensor()
    target_angle = robot_angle + angle
    target_angle = target_angle % 360

    if target_angle < 0:
        target_angle = target_angle + 360

    while True:
        comm = comm_parent.recv()
        motors = motorController.MotorController(comm, 0.05)
        robot_angle = comm.get_imu_sensor()

        diff = target_angle - robot_angle
        direction = 180 - (diff + 360) % 360

        if direction > 0:
            motors.right(speed)
        else:
            motors.left(speed)
        comm_parent.send(comm)

        if abs(diff) < 5:
            motors.brake()
            comm_parent.send(comm)
            return


while True:
    comm = comm_parent.recv()
    motors = motorController.MotorController(comm, 0.05)

    light_sensors = comm.get_light_sensors()
    distance_sensors = comm.get_distance_sensors()
    imu_sensor = comm.get_imu_sensor()

    sensors_on_line = is_line(light_sensors)
    obstacles = is_obstacle(distance_sensors)

    if sensors_on_line:
        if (0 or 7) in sensors_on_line:
            motors.backward(base_speed)
            comm_parent.send(comm)
            sleep(0.1)
            turn(60, base_speed)
        elif 1 in sensors_on_line:
            motors.backward(base_speed)
            comm_parent.send(comm)
            sleep(0.1)
            turn(-60, base_speed)

    elif 0 in obstacles:
        motors.backward(base_speed)
        comm_parent.send(comm)
        sleep(0.1)
        turn(-90, base_speed)
    elif 1 in obstacles:
        motors.backward(base_speed)
        comm_parent.send(comm)
        sleep(0.1)
        turn(-45, base_speed)
    elif 3 in obstacles:
        motors.backward(base_speed)
        comm_parent.send(comm)
        sleep(0.1)
        turn(45, base_speed)

    else:
        motors.forward(base_speed)

    comm_parent.send(comm)
