import numpy as np

from hardwarehandler import HardwareHandler


class SensorsHandler(HardwareHandler):
    def __init__(self, sensors_reader):
        super().__init__(sensors_reader, False)
        self._light_sensors = np.zeros(8)
        self._distance_sensors = np.zeros(5)
        self._imu_sensor = 0

    def update(self):
        if self._event.is_set():
            self._event.clear()
            sensors_data = self._hardware.get_sensors_data()

            self._light_sensors = sensors_data[0][1]
            self._distance_sensors = sensors_data[1][1]
            self._imu_sensor = sensors_data[2][1]

            self._writer.send([self._light_sensors, self._distance_sensors, self._imu_sensor])
