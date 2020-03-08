from time import time


class Timer:
    def __init__(self):
        self._time_start = time()
        self._time_pause_start = 0
        self._time_pause = 0
        self._time_stop = 0
        self.paused = False
        self.stopped = False

    def get_time_sec(self):
        if self.stopped:
            return self._time_stop

        return time() - self._time_start - self._time_pause

    def get_time_ms(self):
        if self.stopped:
            return self._time_stop * 1000

        return (time() - self._time_start - self._time_pause) * 1000

    def pause(self):
        self._time_pause_start = time()
        self.paused = True

    def resume(self):
        self._time_pause += time() - self._time_pause_start
        self._time_pause_start = 0
        self.paused = False

    def stop(self):
        self.stopped = True
        self._time_stop = time() - self._time_start - self._time_pause

    def reset(self):
        self._time_start = time()
        self._time_pause_start = 0
        self._time_pause = 0
