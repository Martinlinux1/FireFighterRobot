from multiprocessing import Pipe

import numpy as np


class Communication:
    def __init__(self, sensors_reader, motor_writer):
        self._sensors_reader = sensors_reader
        self._motor_writer = motor_writer

        self._sensors_pipe_parent, self._sensors_pipe_child = Pipe()
        self._motors_pipe_parent, self._motors_pipe_child = Pipe()

        self._light_sensors = np.int(8)
        self._distance_sensors = np.int(5)
        self._imu_sensor = -999

        self._motorA = []
        self._motorB = []
        self._motorC = []
        self._motorD = []

    def update_sensors(self):
        sensors_data = self._sensors_reader.get_sensors_data()

        self._light_sensors = sensors_data[0][1]
        self._distance_sensors = sensors_data[1][1]
        self._imu_sensor = sensors_data[2][1]

        self._sensors_pipe_parent.send([self._light_sensors, self._distance_sensors, self._imu_sensor])

    def get_sensors(self):
        if self._sensors_pipe_child.poll():
            sensors = self._sensors_pipe_child.recv()
            return sensors

    def update_motors(self):
        if self._motors_pipe_child.poll():
            motors = self._motors_pipe_child.recv()

            if motors[0]:
                self._motor_writer.write_motor('A', motors[0][0], motors[0][1])
            if motors[1]:
                self._motor_writer.write_motor('B', motors[1][0], motors[1][1])
            if motors[2]:
                self._motor_writer.write_motor('C', motors[2][0], motors[2][1])
            if motors[3]:
                self._motor_writer.write_motor('D', motors[3][0], motors[3][1])

    def set_motor(self, motor, direction, speed):
        if motor == 'A':
            self._motorA = [direction, speed]
        elif motor == 'B':
            self._motorB = [direction, speed]
        elif motor == 'C':
            self._motorC = [direction, speed]
        elif motor == 'D':
            self._motorD = [direction, speed]

        self._motors_pipe_parent.send([self._motorA, self._motorB, self._motorC, self._motorD])
