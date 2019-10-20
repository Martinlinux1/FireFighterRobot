import numpy as np


class Communication:
    def __init__(self, communication_handler):
        self._communication_handler = communication_handler
        self._light_sensors = np.int(8)
        self._distance_sensors = np.int(5)
        self._imu_sensor = -999

        self._motorA = []
        self._motorB = []
        self._motorC = []
        self._motorD = []

    def update_sensors(self):
        sensors_data = self._communication_handler.get_sensors_data()
        print(sensors_data)

        self._light_sensors = sensors_data[0][1]
        self._distance_sensors = sensors_data[1][1]
        self._imu_sensor = sensors_data[2][1]

    def get_light_sensors(self):
        return self._light_sensors

    def get_distance_sensors(self):
        return self._distance_sensors

    def get_imu_sensor(self):
        return self._imu_sensor

    def update_motors(self):
        self._communication_handler.write_motor(self._motorA[0], self._motorA[1])
        self._communication_handler.write_motor(self._motorB[0], self._motorB[1])
        self._communication_handler.write_motor(self._motorC[0], self._motorC[1])
        self._communication_handler.write_motor(self._motorD[0], self._motorD[1])

    def set_motor(self, motor, direction, speed):
        if motor == 'A':
            self._motorA = [direction, speed]
        elif motor == 'B':
            self._motorB = [direction, speed]
        elif motor == 'C':
            self._motorC = [direction, speed]
        elif motor == 'D':
            self._motorD = [direction, speed]
