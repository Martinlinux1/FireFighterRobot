import unittest

from IO.commiface import MessageType
from handlers.encoders_handler import EncodersHandler
from handlers.mock.mock_encoders_iface import MockEncodersIface


class TestUpdate(unittest.TestCase):
    def test_update(self):
        encoders_expected_values = [10.2, 10.3, 10.4, 10.5]
        encoders_set_values = [MessageType.ENCODERS, []]
        for v in encoders_expected_values:
            encoders_set_values[1].append(v)

        encoders_iface = MockEncodersIface()
        encoders_handler = EncodersHandler(encoders_iface)

        encoders_iface.set_encoders_data(encoders_set_values)

        encoders_handler.update()

        encoders_values = encoders_handler.get()

        self.assertEqual(encoders_expected_values, encoders_values)


class TestReset(unittest.TestCase):
    def test_reset(self):
        encoders_iface = MockEncodersIface()
        encoders_handler = EncodersHandler(encoders_iface)

        encoders_handler.reset()
        encoders_handler.update()

        self.assertEqual(True, encoders_iface.is_reset())


if __name__ == '__main__':
    unittest.main()
