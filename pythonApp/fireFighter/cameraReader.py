import multiprocessing
import time

import numpy as np
from pyusb2fir import USB2FIR


class CameraReader:
    def __init__(self, thermal_camera: USB2FIR):
        self._thermal_camera = thermal_camera

        self._temp_data_pipe_reader, self._temp_data_pipe_writer = multiprocessing.Pipe(duplex=False)
        self._camera_read_event = multiprocessing.Event()

        self._camera_read_event.set()

        self._temperatures = []

    def update_camera_data(self):
        sub_frame_0 = self._thermal_camera.initializeFrame()
        sub_frame_1 = self._thermal_camera.initializeFrame()
        frame = self._thermal_camera.initializeFrame()
        ts = time.time()
        self._thermal_camera.updateFrame(sub_frame_0)
        self._thermal_camera.updateFrame(sub_frame_1)
        print((time.time() - ts) * 1000)

        for i in range(len(sub_frame_0)):
            if sub_frame_0[i] == 0:
                frame[i] = sub_frame_1[i]
            elif sub_frame_1[i] == 0:
                frame[i] = sub_frame_0[i]

        if self._camera_read_event.is_set():
            self._camera_read_event.clear()
            self._temp_data_pipe_writer.send(frame)

    def get_camera_data(self):
        if self._temp_data_pipe_reader.poll():
            self._camera_read_event.set()
            self._temperatures = self._temp_data_pipe_reader.recv()

        return self._temperatures

    def clear_camera_event(self):
        self._camera_read_event.clear()
        self._temperatures = np.zeros(32 * 24)

    def set_camera_event(self):
        self._camera_read_event.set()
