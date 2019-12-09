from multiprocessing import Pipe


class MotorsLogicCommunication:
    def __init__(self, new_data_event):
        self.forward_char = 'F'
        self.backward_char = 'B'
        self.turn_char = 'T'
        self.slide_char = 'S'
        self.left_char = 'L'
        self.right_char = 'R'
        self.brake_char = 'C'

        self._motors_data = []
        self._new_data_event = new_data_event
        self._data_reader, self._data_writer = Pipe(duplex=False)

    def forward(self, speed):
        message = [self.forward_char, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def backward(self, speed):
        message = [self.backward_char, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def turn(self, angle, speed):
        message = [self.turn_char, angle, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def slide(self, angle, speed):
        message = [self.slide_char, angle, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def left(self, speed):
        message = [self.left_char, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def right(self, speed):
        message = [self.right_char, speed]
        self._data_writer.send(message)
        self._new_data_event.set()

    def brake(self):
        message = [self.brake_char]
        self._data_writer.send(message)
        self._new_data_event.set()

    def data_available(self):
        return self._data_reader.poll()

    def get_data(self):
        if self.data_available():
            self._motors_data = self._data_reader.recv()
        self._new_data_event.clear()
        return self._motors_data
