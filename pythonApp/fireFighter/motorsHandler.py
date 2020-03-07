from hardwarehandler import HardwareHandler


class MotorsHandler(HardwareHandler):
    def __init__(self, motors_writer):
        super().__init__(motors_writer, False)
        self._motors = []
        self._motorA = []
        self._motorB = []
        self._motorC = []
        self._motorD = []

    def update(self):
        if self._reader.poll():
            self._motors = self._reader.recv()

        if self._motors[0] == 0 and self._motors[1] == 0 and self._motors[2] == 0 and self._motors[3] == 0:
            self._hardware.brake()

        if self._motors[0]:
            self._hardware.write_motor('A', self._motors[0][0], self._motors[0][1])
        if self._motors[1]:
            self._hardware.write_motor('B', self._motors[1][0], self._motors[1][1])
        if self._motors[2]:
            self._hardware.write_motor('C', self._motors[2][0], self._motors[2][1])
        if self._motors[3]:
            self._hardware.write_motor('D', self._motors[3][0], self._motors[3][1])

    def set_motor(self, motor, direction, speed):
        if motor == 'A':
            self._motorA = [direction, speed]
        elif motor == 'B':
            self._motorB = [direction, speed]
        elif motor == 'C':
            self._motorC = [direction, speed]
        elif motor == 'D':
            self._motorD = [direction, speed]

    def write(self):
        self._writer.send([self._motorA, self._motorB, self._motorC, self._motorD])