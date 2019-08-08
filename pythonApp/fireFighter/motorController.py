import errors
import MathUtils


class MotorHandler:
    """Handles 4 motors with mecanum wheels motion."""
    def __init__(self, communication_handler):
        self._communicationHandler = communication_handler
        self._mathUtils = MathUtils.MathUtils()

    """Moves the robot forward"""
    def forward(self, speed):
        # Invalid argument.
        if speed > 255:
            raise errors.InvalidArgumentException

        self._communicationHandler.write_motor('A', 'F', speed)
        self._communicationHandler.write_motor('B', 'F', speed)
        self._communicationHandler.write_motor('C', 'F', speed)
        self._communicationHandler.write_motor('D', 'F', speed)

    """Moves the robot backward."""
    def backward(self, speed):
        # Invalid argument.
        if speed > 255:
            raise errors.InvalidArgumentException

        self._communicationHandler.write_motor('A', 'B', speed)
        self._communicationHandler.write_motor('B', 'B', speed)
        self._communicationHandler.write_motor('C', 'B', speed)
        self._communicationHandler.write_motor('D', 'B', speed)

    def left(self, speed):
        self._communicationHandler.write_motor('A', 'B', speed)
        self._communicationHandler.write_motor('B', 'F', speed)
        self._communicationHandler.write_motor('C', 'F', speed)
        self._communicationHandler.write_motor('D', 'B', speed)

    def right(self, speed):
        self._communicationHandler.write_motor('A', 'F', speed)
        self._communicationHandler.write_motor('B', 'B', speed)
        self._communicationHandler.write_motor('C', 'B', speed)
        self._communicationHandler.write_motor('D', 'F', speed)

    """Slides the robot to a given angle."""
    def slide(self, angle, speed):
        if angle >= 0:
            if angle <= 45:
                bc_speed = int(self._mathUtils.valmap(angle, 45, 0, 0, speed))
                print(bc_speed)
                self._communicationHandler.write_motor('A', 'F', speed)
                self._communicationHandler.write_motor('B', 'F', bc_speed)
                self._communicationHandler.write_motor('C', 'F', bc_speed)
                self._communicationHandler.write_motor('D', 'F', speed)
            elif angle <= 90:
                bc_speed = int(self._mathUtils.valmap(angle, 45, 90, 0, speed))
                self._communicationHandler.write_motor('A', 'F', speed)
                self._communicationHandler.write_motor('B', 'B', bc_speed)
                self._communicationHandler.write_motor('C', 'B', bc_speed)
                self._communicationHandler.write_motor('D', 'F', speed)
            elif angle <= 135:
                ad_speed = int(self._mathUtils.valmap(angle, 135, 90, 0, speed))
                self._communicationHandler.write_motor('A', 'F', ad_speed)
                self._communicationHandler.write_motor('B', 'B', speed)
                self._communicationHandler.write_motor('C', 'B', speed)
                self._communicationHandler.write_motor('D', 'F', ad_speed)
            elif angle <= 180:
                bc_speed = int(self._mathUtils.valmap(angle, 135, 180, 0, speed))
                self._communicationHandler.write_motor('A', 'B', speed)
                self._communicationHandler.write_motor('B', 'B', bc_speed)
                self._communicationHandler.write_motor('C', 'B', bc_speed)
                self._communicationHandler.write_motor('D', 'B', speed)

        else:
            if angle >= -45:
                ad_speed = int(self._mathUtils.valmap(angle, -45, 0, 0, speed))
                self._communicationHandler.write_motor('A', 'F', ad_speed)
                self._communicationHandler.write_motor('B', 'F', speed)
                self._communicationHandler.write_motor('C', 'F', speed)
                self._communicationHandler.write_motor('D', 'F', ad_speed)
            elif angle >= -90:
                ad_speed = int(self._mathUtils.valmap(angle, -45, -90, 0, speed))
                self._communicationHandler.write_motor('A', 'B', ad_speed)
                self._communicationHandler.write_motor('B', 'F', speed)
                self._communicationHandler.write_motor('C', 'F', speed)
                self._communicationHandler.write_motor('D', 'B', ad_speed)
            elif angle >= -135:
                bc_speed = int(self._mathUtils.valmap(angle, -135, -90, 0, speed))
                self._communicationHandler.write_motor('A', 'B', speed)
                self._communicationHandler.write_motor('B', 'F', bc_speed)
                self._communicationHandler.write_motor('C', 'F', bc_speed)
                self._communicationHandler.write_motor('D', 'B', speed)
            elif angle >= -180:
                ad_speed = int(self._mathUtils.valmap(angle, -135, -180, 0, speed))
                self._communicationHandler.write_motor('A', 'B', ad_speed)
                self._communicationHandler.write_motor('B', 'B', speed)
                self._communicationHandler.write_motor('C', 'B', speed)
                self._communicationHandler.write_motor('D', 'B', ad_speed)

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
