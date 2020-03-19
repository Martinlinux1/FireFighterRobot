from multiprocessing import Pipe, Event
from abc import ABC, abstractmethod
import numpy as np


class HardwareHandler(ABC):
    @abstractmethod
    def __init__(self, hardware, duplex):
        self._hardware = hardware
        self._value = None
        self._value_set = None
        self._event = Event()
        self._event.set()
        self._duplex = duplex
        if duplex:
            self._main, self._update = Pipe(True)
        else:
            self._reader, self._writer = Pipe(False)

    def get(self):
        if self._duplex:
            if self._main.poll():
                self._value = self._main.recv()
                self._event.set()
        else:
            if self._reader.poll():
                self._value = self._reader.recv()
                self._event.set()

            return self._value

    @abstractmethod
    def update(self):
        pass

    def set(self, value):
        self._value_set = value

    def write(self):
        if self._duplex:
            self._main.send(self._value_set)
