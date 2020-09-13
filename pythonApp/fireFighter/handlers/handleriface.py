from multiprocessing import Pipe, Event
from abc import ABC, abstractmethod


class HandlerIface(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def update(self):
        pass

