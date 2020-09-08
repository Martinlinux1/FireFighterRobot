import unittest

import errors
from IO.commiface import CommInterface
from IO.mock.mock_serial import MockSerial
from IO.motorswriter import MotorsWriter


class TestWriteMotor(unittest.TestCase):
    def test_write_motor_successful(self):
        serial = MockSerial()
        commiface = CommInterface(serial)
        motors_writer = MotorsWriter(commiface)

        response_message = '<M{A,F,255}>\n'
        serial.add_response('~{}'.format(response_message))

        success = motors_writer.write_motor('A', 'F', 255)

        self.assertTrue(success)
        self.assertEqual(response_message, serial.get_sent_message())

    def test_write_motor_invalid_response(self):
        serial = MockSerial()
        commiface = CommInterface(serial)
        motors_writer = MotorsWriter(commiface)

        response_message = 'ncirncierc'
        serial.add_response('~{}'.format(response_message))

        self.assertRaises(errors.InvalidMessageException, motors_writer.write_motor, 'A', 'F', 255)


if __name__ == '__main__':
    unittest.main()
