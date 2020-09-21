from multiprocessing import Pipe, Event

from handlers.handleriface import HandlerIface


class SensorsHandler(HandlerIface):
    def __init__(self, sensors_reader):
        super().__init__()
        self._reader, self._writer = Pipe(duplex=False)
        self._sensors = sensors_reader
        self._sensors_data = []
        self._read_event = Event()
        self._read_event.set()

    def update(self):
        if self._read_event.is_set():
            self._read_event.clear()
            sensors_data = self._sensors.get_sensors_data()

            light_sensors = sensors_data[0][1]
            distance_sensors = sensors_data[1][1]
            imu_sensor = sensors_data[2][1]

            self._writer.send([light_sensors, distance_sensors, imu_sensor])

    def get(self):
        if self._reader.poll():
            self._sensors_data = self._reader.recv()

        return self._sensors_data

    def set(self, value):
        pass
