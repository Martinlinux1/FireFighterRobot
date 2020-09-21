import numpy as np
import random


class MockCamera:
    def __init__(self, num_candles, fire_threshold):
        self._num_candles = num_candles
        self._fire_threshold = fire_threshold

    def initializeFrame(self):
        return np.array([0] * 768)

    def updateFrame(self, frame):
        for i in range(768):
            frame[i] = random.randint(0, self._fire_threshold - 1)

        for i in range(self._num_candles):
            x = random.randint(0, 767)
            frame[x] = random.randint(self._fire_threshold, 300)
            frame[x - 1] = random.randint(self._fire_threshold, 300)
