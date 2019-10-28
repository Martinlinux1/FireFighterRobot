import multiprocessing

import serial

import communication
import communicationHandler
import motorController


def robot_logic(comm_child_pipe):
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

robot_logic_process = multiprocessing.Process(target=robot_logic, args=[comm_child])
comm_parent.send(comm)

robot_logic_process.start()


def turn(angle, speed):
    comm = comm_parent.recv()
    robot_angle = comm.get_imu_sensor()
    target_angle = robot_angle + angle
    target_angle = target_angle % 360

    if target_angle < 0:
        target_angle = target_angle + 360

    while True:
        comm = comm_parent.recv()
        robot_angle = comm.get_imu_sensor()
        print(robot_angle)

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


def is_line(line_sensors):


while True:
    comm = comm_parent.recv()

    light_sensors = comm.get_light_sensors()
    distance_sensors = comm.get_distance_sensors()
    imu_sensor = comm.get_imu_sensor()

    if light_sensors:
