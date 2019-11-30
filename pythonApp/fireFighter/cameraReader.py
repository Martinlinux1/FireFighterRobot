import multiprocessing

from pyusb2fir import USB2FIR


class CameraReader:
    def __init__(self, thermal_camera: USB2FIR):
        self._thermal_camera = thermal_camera

        self._temp_data_pipe_reader, self._temp_data_pipe_writer = multiprocessing.Pipe(duplex=False)

        self._temperatures = []

    def update_camera_data(self):
        sub_frame_0 = self._thermal_camera.initializeFrame()
        sub_frame_1 = self._thermal_camera.initializeFrame()
        frame = self._thermal_camera.initializeFrame()

        self._thermal_camera.updateFrame(sub_frame_0)
        self._thermal_camera.updateFrame(sub_frame_1)

        for i in range(len(sub_frame_0)):
            if sub_frame_0[i] == 0:
                frame[i] = sub_frame_1[i]
            elif sub_frame_1[i] == 0:
                frame[i] = sub_frame_0[i]

        self._temp_data_pipe_writer.send(frame)

    def get_camera_data(self):
        if self._temp_data_pipe_reader.poll():
            self._temperatures = self._temp_data_pipe_reader.recv()

        return self._temperatures
