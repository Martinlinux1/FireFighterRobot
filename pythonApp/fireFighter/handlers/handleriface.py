from multiprocessing import Pipe, Event
from abc import ABC, abstractmethod


class HandlerIface(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self, value):
        pass

    @abstractmethod
    def update(self):
        pass

