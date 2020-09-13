from abc import ABC
from multiprocessing import Pipe

from handlers.handleriface import HandlerIface


class MotorsHandler(HandlerIface):
    def __init__(self, motors_writer):
        super().__init__()
        self._reader, self._writer = Pipe(duplex=False)
        self._motors = motors_writer
        self._motors_values = []
        self._motorA = []
        self._motorB = []
        self._motorC = []
        self._motorD = []

    def update(self):
        if self._reader.poll():
            self._motors_values = self._reader.recv()

        if self._motors_values[0] == 0 and self._motors_values[1] == 0 \
                and self._motors_values[2] == 0 and self._motors_values[3] == 0:
            self._motors.brake()

        if self._motors_values[0]:
            self._motors.write_motor('A', self._motors_values[0][0], self._motors_values[0][1])
        if self._motors_values[1]:
            self._motors.write_motor('B', self._motors_values[1][0], self._motors_values[1][1])
        if self._motors_values[2]:
            self._motors.write_motor('C', self._motors_values[2][0], self._motors_values[2][1])
        if self._motors_values[3]:
            self._motors.write_motor('D', self._motors_values[3][0], self._motors_values[3][1])

    def set(self, value):
        self._writer.send(value)

    def set_motor(self, motor, direction, speed):
        if motor == 'A':
            self._motorA = [direction, speed]
        elif motor == 'B':
            self._motorB = [direction, speed]
        elif motor == 'C':
            self._motorC = [direction, speed]
        elif motor == 'D':
            self._motorD = [direction, speed]

        self.set([self._motorA, self._motorB, self._motorC, self._motorD])

    def get(self):
        pass
