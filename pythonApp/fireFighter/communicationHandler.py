import errors

class CommunicationHandler:
    def __init__(self, seriallink):
        self.serial = seriallink

        self.lightSensor = 'L'
        self.distanceSensor = 'D'
        self.imuSensor = 'I'
        self.motor = 'M'

        self.messageStart = '<'
        self.messageEnd = '>'

        self.dataStart = '{'
        self.dataEnd = '}'

    def write_message(self, message):
        self.serial.write(bytearray(message + '\n', 'ascii'))
        response = self.serial.readline()

        if response.startswith(b'<') and response.endswith(b'\n'):
            return response[:response.find(b'\n')].decode('ascii')
        else:
            raise errors.InvalidMessageException

    def get_light_sensor_data(self, sensor):
        message = self.messageStart + self.lightSensor + self.dataStart + str(sensor) + self.dataEnd + self.messageEnd

        response = self.write_message(message)

        if response[1] == self.lightSensor:
            data = response[response.find(',') + 1:response.find('}', 3)]

            return int(data)
        else:
            raise errors.InvalidMessageException

    def get_distance_sensor_data(self, sensor):
        message = self.messageStart + self.distanceSensor + self.dataStart + str(sensor) + self.dataEnd + self.messageEnd

        response = self.write_message(message)

        if response[1] == self.distanceSensor:
            data = response[response.find(',') + 1:response.find('}', 3)]

            return int(data)
        else:
            raise errors.InvalidMessageException

    def get_imu_sensor_data(self):
        message = self.messageStart + self.imuSensor + self.dataStart + self.dataEnd + self.messageEnd

        response = self.write_message(message)

        if response[1] == self.imuSensor:
            data = response[response.find('{') + 1:response.find('}', 3)]

            return int(data)
        else:
            raise errors.InvalidMessageException

    def write_motor(self, motor, direction, speed):
        message = self.messageStart + self.motor + self.dataStart + motor + "," + direction + "," + str(speed) \
                  + self.dataEnd + self.messageEnd

        response = self.write_message(message)

        if response == message:
            return True
        else:
            raise errors.InvalidMessageException
