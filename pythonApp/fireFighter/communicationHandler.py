import errors


class CommunicationHandler:
    """Handles communication with the sensor interface"""
    def __init__(self, serial_link):
        # serial link
        self._serial = serial_link

        self._lightSensor = 'L'
        self._distanceSensor = 'D'
        self._imuSensor = 'I'
        self._motor = 'M'
        self._echo = 'E'

        self._messageStart = '<'
        self._messageEnd = '>'

        self._dataStart = '{'
        self._dataEnd = '}'

    """Sends message via serial link."""
    def write_message(self, message: str):
        # Write the message.
        self._serial.write(bytearray(message + '\n', 'ascii'))
        # Wait for response.
        response = self._serial.readline()

        # If the response is valid, return it.
        if response.startswith(b'<') and response.endswith(b'\n'):
            return response[:response.find(b'\n')].decode('ascii')
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Reads data from light sensor."""
    def get_light_sensor_data(self, sensor: int):
        # Construct the request.
        message = self._messageStart + self._lightSensor + self._dataStart + str(sensor) + self._dataEnd + \
                  self._messageEnd

        # Send the request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data.
        if response[1] == self._lightSensor:
            data = response[response.find(',') + 1:response.find('}', 3)]

            return int(data)
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Reads data from distance sensor."""
    def get_distance_sensor_data(self, sensor: int):
        # Construct the request.
        message = self._messageStart + self._distanceSensor + self._dataStart + str(sensor) + self._dataEnd + \
                  self._messageEnd

        # Send the request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data
        if response[1] == self._distanceSensor:
            data = response[response.find(',') + 1:response.find('}', 3)]

            return int(data)
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Reads data from imu sensor."""
    def get_imu_sensor_data(self):
        # Construct the request.
        message = self._messageStart + self._imuSensor + self._dataStart + self._dataEnd + self._messageEnd

        # Send request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data.
        if response[1] == self._imuSensor:
            data = response[response.find('{') + 1:response.find('}', 3)]

            return float(data)
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Turns on motor."""
    def write_motor(self, motor, direction, speed):
        # Construct the request.
        message = self._messageStart + self._motor + self._dataStart + motor + "," + direction + "," + str(speed) \
                  + self._dataEnd + self._messageEnd

        # Send request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return true.
        if response == message:
            return True
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    def echo(self):
        message = self._messageStart + self._imuSensor + self._dataStart + self._dataEnd + self._messageEnd

        response = self.write_message(message)

        if response.find('OK'):
            return True
        else:
            return False
