class MockMotorsWriter:
    def __init__(self):
        self._motors_values = []

    def write_motor(self, motor, direction, speed):
        self._motors_values.append([motor, direction, speed])

    def get_motors_values(self):
        return self._motors_values

    def reset_motors_values(self):
        self._motors_values = []
