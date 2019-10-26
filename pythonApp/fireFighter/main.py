import multiprocessing

import serial

import communication
import communicationHandler
import motorController


def robot_logic(sensors_comm_child_pipe, motors_comm_child_pipe):
    motors_c = motors_comm_child_pipe.recv()
    while True:
        sensor_c: communication.Communication = sensors_comm_child_pipe.recv()
        print(sensor_c.get_light_sensors(), sensor_c.get_distance_sensors())
        motors_c.set_motor('A', 'F', 255)
        motors_comm_child_pipe.send(motors_c)


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
sensors_comm: communication.Communication = communication.Communication(comm_handler)
motors_comm: communication.Communication = communication.Communication(comm_handler)

motors = motorController.MotorController(motors_comm, 0.05)

sensors_comm_parent, sensors_comm_child = multiprocessing.Pipe()
motors_comm_parent, motors_comm_child = multiprocessing.Pipe()

robot_logic_process = multiprocessing.Process(target=robot_logic, args=[sensors_comm_child, motors_comm_child])

motors_comm_parent.send(motors_comm)

robot_logic_process.start()

while True:
    sensors_comm.update_sensors()
    sensors_comm_parent.send(sensors_comm)

    motors_comm = motors_comm_parent.recv()
    motors_comm.update_motors()
