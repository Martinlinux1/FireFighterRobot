from multiprocessing import Pipe, Event

from handlers.handleriface import HandlerIface


class EncodersHandler(HandlerIface):
    def __init__(self, encoders_reader):
        super().__init__()
        self._main, self._update = Pipe()
        self._read_event = Event()
        self._read_event.set()

        self._encoders = encoders_reader
        self._encoders_data = []

    def update(self):
        if self._update.poll():
            message = self._update.recv()
            if message == 'R':
                self._encoders.reset()

        if self._read_event.is_set():
            self._read_event.clear()
            try:
                encoders_data = self._encoders.get_encoders_data()[1]
            except IndexError:
                return

            self._update.send(encoders_data)

    def get(self):
        if self._main.poll():
            self._encoders_data = self._main.recv()

        return self._encoders_data

    def set(self, value):
        self._main.send(value)

    def reset(self):
        self.set('R')
