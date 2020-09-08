import unittest

import numpy as np

from IO.commiface import CommInterface
from IO.mock.mock_serial import MockSerial
from IO.sensorsreader import SensorsReader


class TestGetSensorsData(unittest.TestCase):
    def test_get_sensors_data(self):
        serial = MockSerial()
        commiface = CommInterface(serial)
        sensors_reader = SensorsReader(commiface)

        light_sensor_expected_data = np.array([10, 11, 12, 13, 14, 15, 16, 17])
        distance_sensor_expected_data = np.array([10, 11, 12, 13, 14])
        imu_sensor_expected_data = 90.123

        response_message = '<L{'
        for value in light_sensor_expected_data:
            if type(value) == str:
                response_message += value
            else:
                response_message += str(value)
            response_message += ','
        response_message = response_message[:-1]
        response_message += '}>\t'

        response_message += '<D{'
        for value in distance_sensor_expected_data:
            if type(value) == str:
                response_message += value
            else:
                response_message += str(value)
            response_message += ','
        response_message = response_message[:-1]
        response_message += '}>\t'

        response_message += '<I{' + str(imu_sensor_expected_data) + '}>\n'

        serial.add_response('~{}'.format(response_message))

        data = sensors_reader.get_sensors_data()

        self.assertTrue(np.array_equal(light_sensor_expected_data, data[0][1]))
        self.assertTrue(np.array_equal(distance_sensor_expected_data, data[1][1]))
        self.assertEqual(imu_sensor_expected_data, data[2][1])


if __name__ == '__main__':
    unittest.main()
