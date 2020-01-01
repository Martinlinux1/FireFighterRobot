import multiprocessing

from pyusb2fir import USB2FIR


class CameraReader:
    def __init__(self, thermal_camera: USB2FIR):
        self._thermal_camera = thermal_camera

        self._temp_data_pipe_reader, self._temp_data_pipe_writer = multiprocessing.Pipe(duplex=False)
        self._camera_read_event = multiprocessing.Event()

        self._camera_read_event.set()

        self._temperatures = []

    def update_camera_data(self):
        frame = self._thermal_camera.initializeFrame()

        self._thermal_camera.updateFrame(frame)

        if self._camera_read_event.is_set():
            self._camera_read_event.clear()
            print('sending frame')
            self._temp_data_pipe_writer.send(frame)

    def get_camera_data(self):
        if self._temp_data_pipe_reader.poll():
            self._camera_read_event.set()
            self._temperatures = self._temp_data_pipe_reader.recv()

        return self._temperatures
