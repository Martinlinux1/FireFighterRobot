import unittest

from IO.commiface import MessageType
from handlers.mock.mock_sensorsreader import MockSensorsReader
from handlers.sensorsHandler import SensorsHandler


class TestUpdate(unittest.TestCase):
    def test_update(self):
        sensors_expected_values = [[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5], 90.12]
        sensors_set_values = [[MessageType.LIGHT_SENSOR, sensors_expected_values[0]],
                              [MessageType.DISTANCE_SENSOR, sensors_expected_values[1]],
                              [MessageType.IMU_SENSOR, sensors_expected_values[2]]]

        sensors_reader = MockSensorsReader()
        sensors_handler = SensorsHandler(sensors_reader)

        sensors_reader.set_sensors_data(sensors_set_values)

        sensors_handler.update()

        sensors_values = sensors_handler.get()

        self.assertEqual(sensors_expected_values, sensors_values)


class TestGet(unittest.TestCase):
    def test_get(self):
        sensors_expected_values = [[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5], 90.12]
        sensors_set_values = [[MessageType.LIGHT_SENSOR, sensors_expected_values[0]],
                              [MessageType.DISTANCE_SENSOR, sensors_expected_values[1]],
                              [MessageType.IMU_SENSOR, sensors_expected_values[2]]]
        sensors_reader = MockSensorsReader()
        sensors_handler = SensorsHandler(sensors_reader)

        sensors_reader.set_sensors_data(sensors_set_values)

        sensors_handler.update()

        sensors_values = sensors_handler.get()

        self.assertEqual(sensors_expected_values, sensors_values)

    def test_get_blank(self):
        sensors_expected_values = []
        sensors_reader = MockSensorsReader()
        sensors_handler = SensorsHandler(sensors_reader)

        sensors_values = sensors_handler.get()

        self.assertEqual(sensors_expected_values, sensors_values)


if __name__ == '__main__':
    unittest.main()
