import multiprocessing

import serial

import communication
import communicationHandler
import motorController


def robot_logic(comm_child_pipe):
    motors_c = comm_child_pipe.recv()
    while True:
        c: communication.Communication = comm_child_pipe.recv()
        print(c.get_light_sensors(), c.get_distance_sensors())
        c.set_motor('A', 'F', 255)
        comm_child_pipe.send(c)


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
comm: communication.Communication = communication.Communication(comm_handler)

motors = motorController.MotorController(comm, 0.05)

comm_parent, comm_child = multiprocessing.Pipe()

robot_logic_process = multiprocessing.Process(target=robot_logic, args=[comm_child])

comm_parent.send(comm)

robot_logic_process.start()

while True:
    comm.update_sensors()
    comm_parent.send(comm)

    comm = comm_parent.recv()
    comm.update_motors()
