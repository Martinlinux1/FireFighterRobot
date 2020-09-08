import unittest

import numpy as np

import errors
from IO.commiface import CommInterface
from IO.encodersiface import EncodersInterface
from IO.mock.mock_serial import MockSerial


class TestGetEncodersData(unittest.TestCase):
    def test_get_sensors_data(self):
        serial = MockSerial()
        commiface = CommInterface(serial)
        encoders_iface = EncodersInterface(commiface)

        encoders_expected_data = np.array([10.23, 11.51, 12.87, 13.09])

        response_message = '<N{'
        for value in encoders_expected_data:
            if type(value) == str:
                response_message += value
            else:
                response_message += str(value)
            response_message += ','
        response_message = response_message[:-1]
        response_message += '}>\n'

        serial.add_response('~{}'.format(response_message))

        data = encoders_iface.get_encoders_data()

        self.assertTrue(np.array_equal(encoders_expected_data, data[1]))


class TestResetEncoders(unittest.TestCase):
    def test_brake_successful(self):
        serial = MockSerial()
        commiface = CommInterface(serial)
        encoders_iface = EncodersInterface(commiface)

        response_message = '<N{R}>\n'
        serial.add_response('~{}'.format(response_message))

        success = encoders_iface.reset_encoders()

        self.assertTrue(success)
        self.assertEqual(response_message, serial.get_sent_message())

    def test_brake_invalid_response(self):
        serial = MockSerial()
        commiface = CommInterface(serial)
        encoders_iface = EncodersInterface(commiface)

        response_message = 'ncirncierc'
        serial.add_response('~{}'.format(response_message))

        self.assertRaises(errors.InvalidMessageException, encoders_iface.reset_encoders)


if __name__ == '__main__':
    unittest.main()
