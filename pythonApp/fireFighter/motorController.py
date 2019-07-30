import errors


class MotorHandler:
    """Handles motor motion."""
    def __init__(self, communication_handler):
        self._communicationHandler = communication_handler

    """Moves two motors forward"""
    def forward(self, motors, speed):
        # Invalid argument.
        if speed > 255:
            raise errors.InvalidArgumentException

        # If motors to run are A and B.
        if motors == 'AB' or motors == 'BA':
            self._communicationHandler.write_motor('A', 'F', speed)
            self._communicationHandler.write_motor('B', 'F', speed)
            self._communicationHandler.write_motor('C', 'F', speed / 2)
            self._communicationHandler.write_motor('D', 'B', speed / 2)

        # If motors to run are C and D
        elif motors == 'CD' or motors == 'DC':
            self._communicationHandler.write_motor('C', 'F', speed)
            self._communicationHandler.write_motor('D', 'F', speed)
            self._communicationHandler.write_motor('A', 'F', speed / 2)
            self._communicationHandler.write_motor('B', 'B', speed / 2)

        # Invalid arguments.
        else:
            raise errors.InvalidArgumentException

    """Moves two motors backward."""
    def backward(self, motors, speed):
        # Invalid argument.
        if speed > 255:
            raise errors.InvalidArgumentException

        # If motors to run are A and B.
        if motors == 'AB' or motors == 'BA':
            self._communicationHandler.write_motor('A', 'B', speed)
            self._communicationHandler.write_motor('B', 'B', speed)
            self._communicationHandler.write_motor('C', 'B', speed / 2)
            self._communicationHandler.write_motor('D', 'F', speed / 2)

        # If motors to run are C and D.
        elif motors == 'CD' or motors == 'DC':
            self._communicationHandler.write_motor('C', 'B', speed)
            self._communicationHandler.write_motor('D', 'B', speed)
            self._communicationHandler.write_motor('A', 'B', speed / 2)
            self._communicationHandler.write_motor('B', 'F', speed / 2)

        # Invalid arguments.
        else:
            raise errors.InvalidArgumentException

    """Turns the robot to a given angle"""
    def turn(self, angle, speed):
        # Invalid arguments.
        if angle > 180 or angle < -180 or speed > 255:
            raise errors.InvalidArgumentException

        else:
            # Current angle of robot.
            robot_angle = self._communicationHandler.get_imu_sensor_data()
            # Target angle of the robot.
            target_angle = robot_angle + angle

            # If desired turn direction is right -> angle > 0.
            if target_angle > robot_angle:
                # Turn the robot until it's current angle is target angle.
                while self._communicationHandler.get_imu_sensor_data() < target_angle - 5:
                    self._communicationHandler.write_motor('A', 'F', speed)
                    self._communicationHandler.write_motor('B', 'B', speed)
                    self._communicationHandler.write_motor('C', 'F', speed)
                    self._communicationHandler.write_motor('D', 'B', speed)
                # Stop motors.
                self.brake()

            # If desired turn direction is left -> angle < 0.
            elif target_angle < robot_angle:
                # Turn the robot until it's current angle is target angle.
                while self._communicationHandler.get_imu_sensor_data() > target_angle - 5:
                    self._communicationHandler.write_motor('A', 'B', speed)
                    self._communicationHandler.write_motor('B', 'F', speed)
                    self._communicationHandler.write_motor('C', 'B', speed)
                    self._communicationHandler.write_motor('D', 'F', speed)
                # stop motors.
                self.brake()

    """Turns the robot until externally stopped."""
    def turn(self, direction, speed):
        if direction == 'L':
            self._communicationHandler.write_motor('A', 'B', speed)
            self._communicationHandler.write_motor('B', 'F', speed)
            self._communicationHandler.write_motor('C', 'B', speed)
            self._communicationHandler.write_motor('D', 'F', speed)
        elif direction == 'R':
            self._communicationHandler.write_motor('A', 'F', speed)
            self._communicationHandler.write_motor('B', 'B', speed)
            self._communicationHandler.write_motor('C', 'F', speed)
            self._communicationHandler.write_motor('D', 'B', speed)

    """Stops all motors."""
    def brake(self):
        self._communicationHandler.write_motor('A', 'F', 0)
        self._communicationHandler.write_motor('B', 'F', 0)
        self._communicationHandler.write_motor('C', 'F', 0)
        self._communicationHandler.write_motor('D', 'F', 0)
