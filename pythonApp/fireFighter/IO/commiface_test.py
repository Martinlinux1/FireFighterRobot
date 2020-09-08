import unittest

import numpy as np

import errors
from IO.mock.mock_serial import MockSerial
from IO.commiface import CommInterface, MessageType


class TestWriteMessage(unittest.TestCase):
    def test_write_message_successful(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        test_message = '~<test_message>'
        response_text = '<test_response>'
        serial.add_response('~{}\n'.format(response_text))

        response = commiface.write_message(test_message)

        self.assertEqual(response_text, response)
        self.assertEqual(test_message + '\n', serial.get_sent_message())

    def test_write_message_invalid_response(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        test_message = '~<test_message>'
        serial.add_response('invalid\n')

        self.assertRaises(errors.InvalidMessageException, commiface.write_message, test_message)


class TestEncodeMessage(unittest.TestCase):
    def test_encode_message_data_present(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        data = ['A', 'F', 255]
        data_str = ''
        for value in data:
            if type(value) == str:
                data_str += value
            else:
                data_str += str(value)
            data_str += ','
        data_str = data_str[:-1]

        expected_encoded_message = '<' + str(MessageType.MOTOR.value) + '{' + data_str + '}' + '>'
        encoded_message = commiface.encode_message(MessageType.MOTOR, data)

        self.assertEqual(expected_encoded_message, encoded_message)

    def test_encode_message_data_not_present(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        expected_encoded_message = '<' + str(MessageType.MOTOR.value) + '{}>'
        encoded_message = commiface.encode_message(MessageType.MOTOR)

        self.assertEqual(expected_encoded_message, encoded_message)


class TestDecodeMessage(unittest.TestCase):
    def test_decode_message_light_sensor(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        expected_values = np.array([10, 11, 12, 13, 14, 15, 16, 17])

        message = '<L{'
        for value in expected_values:
            message += str(value) + ','
        message = message[:-1]
        message += '}>'

        values = commiface.decode_message(message)

        self.assertEqual(MessageType.LIGHT_SENSOR, values[0])
        self.assertTrue(np.array_equal(expected_values, values[1]))

    def test_decode_message_distance_sensor(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        expected_values = np.array([10, 11, 12, 13, 14])

        message = '<D{'
        for value in expected_values:
            message += str(value) + ','
        message = message[:-1]
        message += '}>'

        values = commiface.decode_message(message)

        self.assertEqual(MessageType.DISTANCE_SENSOR, values[0])
        self.assertTrue(np.array_equal(expected_values, values[1]))

    def test_decode_message_imu_sensor(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        expected_value = 90.123

        message = '<I{' + str(expected_value) + '}>'

        values = commiface.decode_message(message)

        self.assertEqual(MessageType.IMU_SENSOR, values[0])
        self.assertEqual(expected_value, values[1])

    def test_decode_message_encoders(self):
        serial = MockSerial()
        commiface = CommInterface(serial)

        expected_values = np.array([10, 11, 12, 13])

        message = '<N{'
        for value in expected_values:
            message += str(value) + ','
        message = message[:-1]
        message += '}>'

        values = commiface.decode_message(message)

        self.assertEqual(MessageType.ENCODERS, values[0])
        self.assertTrue(np.array_equal(expected_values, values[1]))


if __name__ == '__main__':
    unittest.main()
