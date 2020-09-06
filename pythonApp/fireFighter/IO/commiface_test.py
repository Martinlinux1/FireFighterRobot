import unittest

import errors
from IO.mock.mock_serial import MockSerial
from IO.commiface import CommInterface


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


if __name__ == '__main__':
    unittest.main()
