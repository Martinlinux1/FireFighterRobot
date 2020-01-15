from time import time


class Timer:
    def __init__(self):
        self._time_start = time()
        self._time_pause_start = 0
        self._time_pause = 0

    def get_time_sec(self):
        return time() - self._time_start - self._time_pause

    def get_time_ms(self):
        return (time() - self._time_start - self._time_pause) * 1000

    def pause(self):
        self._time_pause_start = time()

    def resume(self):
        self._time_pause += time() - self._time_pause_start

    def reset(self):
        self._time_start = time()
        self._time_pause_start = 0
        self._time_pause = 0
