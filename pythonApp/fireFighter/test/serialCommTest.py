import unittest
from IO import communicationInterface


class MyTestCase(unittest.TestCase):
    def test_motors(self):
        fakeserial = fakeSerial.FakeSerial()

        fakeserial.set_message_to_send("<M{A,F,100}>")

        serial = communicationInterface.CommunicationInterface(fakeserial)

        serial.write_motor('A', 'F', 100)

        sentMessage = fakeserial.get_received_message()
        self.assertEqual(sentMessage, "<M{A,F,100}>")

    def test_light_sensors(self):
        fakeserial = fakeSerial.FakeSerial()

        fakeserial.set_message_to_send("<L{1,1024}>")

        serial = communicationInterface.CommunicationInterface(fakeserial)

        lightSensorData = serial.get_light_sensor_data(0)

        self.assertEqual(lightSensorData, 1024)

    def test_distance_sensors(self):
        fakeserial = fakeSerial.FakeSerial()

        fakeserial.set_message_to_send("<D{0,43}>")

        serial = communicationInterface.CommunicationInterface(fakeserial)

        distanceSensorData = serial.get_distance_sensor_data(0)

        self.assertEqual(distanceSensorData, 43)

    def test_imu_sensor(self):
        fakeserial = fakeSerial.FakeSerial()

        fakeserial.set_message_to_send("<I{20}>")

        serial = communicationInterface.CommunicationInterface(fakeserial)

        imu_data = serial.get_imu_sensor_data()

        self.assertEqual(imu_data, 20)


if __name__ == '__main__':
    unittest.main()
