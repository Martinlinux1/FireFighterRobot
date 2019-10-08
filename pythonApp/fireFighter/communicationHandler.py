import serial

import errors


class CommunicationHandler:
    """Handles communication with the sensor interface"""
    def __init__(self, serial_link: serial.Serial):
        # serial link
        self._serial = serial_link

        self.lightSensor = 'L'
        self.distanceSensor = 'D'
        self.imuSensor = 'I'
        self.motor = 'M'
        self.echo = 'E'
        self.lightSensorsCalibration = 'C'

        self._imuReset = 'R'

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

    def read_message(self):
        message = self._serial.read(self._serial.in_waiting)
        message = message.decode('ascii')
        message = message[message.rfind('~') + 1:]
        message = message.split('\t')

        return message

    def decode_message(self, message: str):
        if '\r' in message:
            message = message[:message.find('\r')]

        if message.startswith('<') and message.endswith('>'):
            if message[1] == self.lightSensor:
                data = message[message.find('{') + 1:message.find('}', 3)]

                light_sensors_values = []

                data = data.split(',')

                for sensor_value in data:
                    try:
                        light_sensors_values.append(int(sensor_value))
                    except ValueError:
                        pass

                return self.lightSensor, light_sensors_values
            elif message[1] == self.distanceSensor:
                data = message[message.find('{') + 1:message.find('}', 3)]

                distance_sensors_values = []

                data = data.split(',')

                for sensor_value in data:
                    try:
                        distance_sensors_values.append(int(sensor_value))
                    except ValueError:
                        pass

                return self.distanceSensor, distance_sensors_values
            elif message[1] == self.imuSensor:
                data = message[message.find('{') + 1:message.find('}', 3)]

                angle = float(data)

                if angle < 0:
                    return self.imuSensor, 2 * 180 + angle
                else:
                    return self.imuSensor, angle
            elif message[1] == self.motor:
                return self.motor, message
            elif message[1] == self.lightSensorsCalibration:
                return self.lightSensorsCalibration, message
            else:
                raise errors.InvalidMessageException

    """Reads data from light sensor."""
    def get_light_sensor_data(self, sensor: int):
        # Construct the request.
        message = self._messageStart + self.lightSensor + self._dataStart + str(sensor) + self._dataEnd + \
                  self._messageEnd

        # Send the request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data.
        if response[1] == self.lightSensor:
            data = response[response.find(',') + 1:response.find('}', 3)]

            return int(data)
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    def get_light_sensors_data(self):
        # Construct the request.
        message = self._messageStart + self.lightSensor + self._dataStart + self._dataEnd + self._messageEnd

        # Send the request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data.
        if response[1] == self.lightSensor:
            data = response[response.find('{') + 1:response.find('}', 3)]

            light_sensors_values = []

            data = data.split(',')

            for sensor_value in data:
                try:
                    light_sensors_values.append(int(sensor_value))
                except ValueError:
                    pass

            return light_sensors_values
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    def calibrate_light_sensors(self):
        # Construct the request.
        message = self._messageStart + self.lightSensorsCalibration + self._dataStart + self._dataEnd + \
                  self._messageEnd

        self._serial.write(bytearray(message + '\n', 'ascii'))

    """Reads data from distance sensor."""
    def get_distance_sensor_data(self, sensor: int):
        # Construct the request.
        message = self._messageStart + self.distanceSensor + self._dataStart + str(sensor) + self._dataEnd + \
                  self._messageEnd

        # Send the request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data
        if response[1] == self.distanceSensor:
            data = response[response.find(',') + 1:response.find('}', 3)]

            return int(data)
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Reads data from imu sensor."""
    def get_imu_sensor_data(self):
        # Construct the request.
        message = self._messageStart + self.imuSensor + self._dataStart + self._dataEnd + self._messageEnd

        # Send request and wait for response.
        response = self.write_message(message)

        # If the response is valid, return sent data.
        if response[1] == self.imuSensor:
            data = response[response.find('{') + 1:response.find('}', 3)]

            angle = float(data)

            if angle < 0:
                return 2 * 180 + angle
            else:
                return angle
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    """Turns on motor."""
    def write_motor(self, motor, direction, speed):
        # Construct the request.
        message = self._messageStart + self.motor + self._dataStart + motor + "," + direction + "," + str(speed) \
                  + self._dataEnd + self._messageEnd

        self._serial.write(bytearray(message + '\n', 'ascii'))

    def echo(self):
        message = self._messageStart + self.imuSensor + self._dataStart + self._dataEnd + self._messageEnd

        response = self.write_message(message)

        if response.find('OK'):
            return True
        else:
            return False
