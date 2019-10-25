import multiprocessing

import serial

import communication
import communicationHandler
import motorController


def robot_logic(comm_q):
    while True:
        c = comm_q.get()
        print(c.get_light_sensors(), c.get_distance_sensors())
        c.set_motor('A', 'F', 200)
        comm_q.put(c)


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
comm = communication.Communication(comm_handler)

motors = motorController.MotorController(comm, 0.05)

comm_queue = multiprocessing.Queue()
robot_logic_process = multiprocessing.Process(target=robot_logic, args=[comm_queue])
robot_logic_process.start()

while True:
    comm.update_sensors()
    comm_queue.put(comm)
    comm = comm_queue.get()
    print('updating motors')
    comm.update_motors()
