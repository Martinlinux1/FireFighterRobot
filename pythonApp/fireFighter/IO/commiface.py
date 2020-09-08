from enum import Enum

import numpy as np
import serial

import errors


class MessageType(Enum):
    LIGHT_SENSOR = 'L'
    DISTANCE_SENSOR = 'D'
    IMU_SENSOR = 'I'
    MOTOR = 'M'
    ECHO = 'E'
    SENSORS_DATA = 'A'
    MOTORS_BRAKE = 'B'
    ENCODERS = 'N'


class CommInterface:
    """Handles communication with the sensor interface"""
    def __init__(self, serial_link):
        self.serial = serial_link

        self._commStart = b'~'
        self._messageStart = '<'
        self._messageEnd = '>'

        self._dataStart = '{'
        self._dataEnd = '}'

        self._elementsSeparator = ','

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
        if response.startswith(self._commStart) and response.endswith(b'\n'):
            return response[response.find(self._commStart) + 1:response.find(b'\n')].decode('ascii')
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Encodes the message."""
    def encode_message(self, message_type: MessageType, data=''):
        message = self._messageStart

        message += message_type.value

        message += self._dataStart + str(data) + self._dataEnd + self._messageEnd

        return message

    """Decodes the message."""
    def decode_message(self, message: str):
        # Remove all newline characters from message.
        message.rstrip()

        if message.startswith(self._messageStart) and message.endswith(self._messageEnd):
            if message[1] == MessageType.LIGHT_SENSOR.value:
                data = message[message.find(self._dataStart) + 1:message.find(self._dataEnd, 3)]

                data = np.array(data.split(self._elementsSeparator))

                light_sensors_values = data.astype(int)

                return MessageType.LIGHT_SENSOR, light_sensors_values
            elif message[1] == MessageType.DISTANCE_SENSOR.value:
                data = message[message.find(self._dataStart) + 1:message.find(self._dataEnd, 3)]

                data = np.array(data.split(self._elementsSeparator))

                distance_sensors_values = data.astype(int)

                return MessageType.DISTANCE_SENSOR, distance_sensors_values
            elif message[1] == MessageType.IMU_SENSOR.value:
                data = message[message.find(self._dataStart) + 1:message.find(self._dataEnd, 3)]

                angle = float(data)

                if angle < 0:
                    return MessageType.IMU_SENSOR, 2 * 180 + angle
                else:
                    return MessageType.IMU_SENSOR, angle
            elif message[1] == MessageType.ENCODERS.value:
                data = message[message.find(self._dataStart) + 1:message.find(self._dataEnd, 3)]

                data = np.array(data.split(self._elementsSeparator))

                encoders_values = data.astype(float)

                return MessageType.ENCODERS, encoders_values
            else:
                raise errors.InvalidMessageException

    """Sends test message and waits for response."""
    def echo(self):
        message = self._messageStart + str(MessageType.ECHO) + self._dataStart + self._dataEnd + self._messageEnd

        response = self.write_message(message)

        if response.find('OK'):
            return True
        else:
            return False
