from multiprocessing import Pipe, Event

import numpy as np
import zmq


class HardwareHandler:
    def __init__(self, sensors_reader, motor_writer):
        self._sensors_reader = sensors_reader
        self._motor_writer = motor_writer

        self._port = "8080"
        self._context_server = zmq.Context()
        self._context_client = zmq.Context()

        self._socket_main_process = self._context_server.socket(zmq.PAIR)
        self._socket_sensors_process = self._context_client.socket(zmq.PAIR)

        self._motors_pipe_reader, self._motors_pipe_writer = Pipe(duplex=False)

        self._sensors_read_event = Event()

        self._sensors_read_event.set()

        self._light_sensors = np.int(8)
        self._distance_sensors = np.int(5)
        self._imu_sensor = -999

        self._sensors = [0, 0, 0]
        self._motors = [0, 0, 0, 0]

        self._motorA = []
        self._motorB = []
        self._motorC = []
        self._motorD = []

    def update_sensors(self):
        self._socket_main_process.bind("tcp://*:5555")
        if self._sensors_read_event.is_set():
            sensors_data = self._sensors_reader.get_sensors_data()

            self._light_sensors = sensors_data[0][1]
            self._distance_sensors = sensors_data[1][1]
            self._imu_sensor = sensors_data[2][1]

            self._socket_main_process.send([self._light_sensors, self._distance_sensors, self._imu_sensor])
        self._socket_main_process.close()

    def get_sensors(self):
        self._socket_sensors_process.bind("tcp://*:5555")
        self._sensors = self._socket_sensors_process.recv()
        self._socket_sensors_process.close()
        return self._sensors

    def update_motors(self):
        if self._motors_pipe_reader.poll():
            self._motors = self._motors_pipe_reader.recv()

        if self._motors[0]:
            self._motor_writer.write_motor('A', self._motors[0][0], self._motors[0][1])
        if self._motors[1]:
            self._motor_writer.write_motor('B', self._motors[1][0], self._motors[1][1])
        if self._motors[2]:
            self._motor_writer.write_motor('C', self._motors[2][0], self._motors[2][1])
        if self._motors[3]:
            self._motor_writer.write_motor('D', self._motors[3][0], self._motors[3][1])

    def set_motor(self, motor, direction, speed):
        if motor == 'A':
            self._motorA = [direction, speed]
        elif motor == 'B':
            self._motorB = [direction, speed]
        elif motor == 'C':
            self._motorC = [direction, speed]
        elif motor == 'D':
            self._motorD = [direction, speed]

    def write_motors(self):
        self._motors_pipe_writer.send([self._motorA, self._motorB, self._motorC, self._motorD])
