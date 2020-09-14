class MockSensorsReader:
    def __init__(self):
        self._sensors_values = []

    def get_sensors_data(self):
        return self._sensors_values

    def set_sensors_data(self, values):
        self._sensors_values = values
