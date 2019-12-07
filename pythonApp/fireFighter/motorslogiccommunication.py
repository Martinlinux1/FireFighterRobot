from multiprocessing import Pipe


class MotorsLogicCommunication:
    def __init__(self, new_data_event):
        self.forward = 'F'
        self.backward = 'B'
        self.turn = 'T'
        self.slide = 'S'
        self.left = 'L'
        self.right = 'R'
        self.brake = 'C'

        self._motors_data = []
        self._new_data_event = new_data_event
        self._data_reader, self._data_writer = Pipe(duplex=False)

    def forward(self, speed):
        message = [self.forward, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def backward(self, speed):
        message = [self.backward, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def turn(self, angle, speed):
        message = [self.turn, angle, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def slide(self, angle, speed):
        message = [self.slide, angle, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def left(self, speed):
        message = [self.left, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def right(self, speed):
        message = [self.right, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def brake(self):
        message = [self.right]
        self._data_writer.send(message)
        self._new_data_event.set()

    def data_available(self):
        return self._data_reader.poll()

    def get_data(self):
        if self.data_available():
            self._motors_data = self._data_reader.recv()
        self._new_data_event.clear()
        return self._motors_data
