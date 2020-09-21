import unittest

from handlers.mock.mock_motorswriter import MockMotorsWriter
from handlers.motors_handler import MotorsHandler


class TestUpdate(unittest.TestCase):
    def test_update_1_motor(self):
        motor_expected_value = ['A', 'F', 127]
        motors_writer = MockMotorsWriter()
        motors_handler = MotorsHandler(motors_writer)
        motors_handler.set([[motor_expected_value[1], motor_expected_value[2]]])

        motors_handler.update()

        motors_values = motors_writer.get_motors_values()

        self.assertEqual(motor_expected_value, motors_values[0])

    def test_update_4_motors(self):
        motors_expected_value = [['A', 'F', 127], ['B', 'F', 127], ['C', 'F', 127], ['D', 'F', 127]]
        motors_writer = MockMotorsWriter()
        motors_handler = MotorsHandler(motors_writer)
        motors_set_values = []
        for motor in motors_expected_value:
            motors_set_values.append([motor[1], motor[2]])

        motors_handler.set(motors_set_values)

        motors_handler.update()

        motors_values = motors_writer.get_motors_values()

        self.assertEqual(motors_expected_value, motors_values)


class TestSetMotor(unittest.TestCase):
    def test_set_motor(self):
        motor_expected_value = ['A', 'F', 127]
        motors_writer = MockMotorsWriter()
        motors_handler = MotorsHandler(motors_writer)
        motors_handler.set_motor(motor_expected_value[0], motor_expected_value[1], motor_expected_value[2])

        motors_handler.update()

        motors_values = motors_writer.get_motors_values()

        self.assertEqual(motor_expected_value, motors_values[0])


if __name__ == '__main__':
    unittest.main()
