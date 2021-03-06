import numpy as np
import serial

import errors


class CommunicationHandler:
    """Handles communication with the sensor interface"""

    def __init__(self, serial_link: serial.Serial):
        # serial link
        self.serial = serial_link

        self.lightSensor = 'L'
        self.distanceSensor = 'D'
        self.imuSensor = 'I'
        self.motor = 'M'
        self.echo = 'E'
        self.sensors_data = 'A'
        self.motors_brake = 'B'
        self.encoders = 'N'

        self._messageStart = '<'
        self._messageEnd = '>'

        self._dataStart = '{'
        self._dataEnd = '}'

    """Sends message via serial link."""
    def write_message(self, message: str):
        if not self.serial.is_open:
            self.serial.open()

        self.serial.flush()
        # Write the message.
        self.serial.write(bytes(message + '\n', 'ascii'))
        # Wait for response.
        response = self.serial.readline()
        self.serial.close()

        # If the response is valid, return it.
        if response.startswith(b'~') and response.endswith(b'\n'):
            return response[response.find(b'~') + 1:response.find(b'\n')].decode('ascii')
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Encodes the message."""
    def encode_message(self, message_type, data=''):
        message = self._messageStart

        message += message_type

        message += self._dataStart + str(data) + self._dataEnd + self._messageEnd

        return message

    """Decodes the message."""
    def decode_message(self, message: str):
        if '\r' in message:
            message = message[:message.find('\r')]

        if message.startswith('<') and message.endswith('>'):
            if message[1] == self.lightSensor:
                data = message[message.find('{') + 1:message.find('}', 3)]

                data = np.array(data.split(','))

                light_sensors_values = data.astype(int)

                return self.lightSensor, light_sensors_values
            elif message[1] == self.distanceSensor:
                data = message[message.find('{') + 1:message.find('}', 3)]

                data = np.array(data.split(','))

                distance_sensors_values = data.astype(int)

                return self.distanceSensor, distance_sensors_values
            elif message[1] == self.imuSensor:
                data = message[message.find('{') + 1:message.find('}', 3)]

                angle = float(data)

                if angle < 0:
                    return self.imuSensor, 2 * 180 + angle
                else:
                    return self.imuSensor, angle
            elif message[1] == self.encoders:
                data = message[message.find('{') + 1:message.find('}', 3)]

                data = np.array(data.split(','))

                encoders_values = data.astype(float)

                return self.encoders, encoders_values

            elif message[1] == self.motor:
                return self.motor, message

            else:
                raise errors.InvalidMessageException

    """Sends test message and waits for response."""
    def echo(self):
        message = self._messageStart + self.imuSensor + self._dataStart + self._dataEnd + self._messageEnd

        response = self.write_message(message)

        if response.find('OK'):
            return True
        else:
            return False
