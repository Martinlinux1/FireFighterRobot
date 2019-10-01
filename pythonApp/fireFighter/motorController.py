from time import sleep
import errors
import communicationHandler
import MathUtils


class MotorController:
    """Handles 4 motors with mecanum wheels motion."""
    def __init__(self, communication_handler, brake_delay):
        self._communicationHandler: communicationHandler.CommunicationHandler = communication_handler
        self._mathUtils = MathUtils.MathUtils()
        self._brake_delay = brake_delay

    """Moves the robot forward"""
    def forward(self, speed: int):
        # Invalid argument.
        if speed > 255:
            raise errors.InvalidArgumentException

        self._communicationHandler.write_motor('A', 'F', speed)
        self._communicationHandler.write_motor('B', 'F', speed)
        self._communicationHandler.write_motor('C', 'F', speed)
        self._communicationHandler.write_motor('D', 'F', speed)

    """Moves the robot backward."""
    def backward(self, speed: int):
        # Invalid argument.
        if speed > 255:
            raise errors.InvalidArgumentException

        self._communicationHandler.write_motor('A', 'B', speed)
        self._communicationHandler.write_motor('B', 'B', speed)
        self._communicationHandler.write_motor('C', 'B', speed)
        self._communicationHandler.write_motor('D', 'B', speed)

    def left(self, speed: int):
        self._communicationHandler.write_motor('A', 'B', speed)
        self._communicationHandler.write_motor('B', 'F', speed)
        self._communicationHandler.write_motor('C', 'F', speed)
        self._communicationHandler.write_motor('D', 'B', speed)

    def right(self, speed: int):
        self._communicationHandler.write_motor('A', 'F', speed)
        self._communicationHandler.write_motor('B', 'B', speed)
        self._communicationHandler.write_motor('C', 'B', speed)
        self._communicationHandler.write_motor('D', 'F', speed)

    """Slides the robot to a given angle."""
    def slide(self, angle: float, speed: int):
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
    def turn(self, angle: float, speed: int):
        # Invalid arguments.
        if angle > 180.0 or angle < -180.0 or speed > 255.0:
            raise errors.InvalidArgumentException
        else:
            robot_angle = self._communicationHandler.get_imu_sensor_data()
            target_angle = robot_angle + angle
            target_angle = target_angle % 360

            if target_angle < 0:
                target_angle = target_angle + 360

            while True:
                robot_angle = self._communicationHandler.get_imu_sensor_data()

                diff = target_angle - robot_angle
                direction = 180 - (diff + 360) % 360

                if direction > 0:
                    self._communicationHandler.write_motor('A', 'F', speed)
                    self._communicationHandler.write_motor('B', 'B', speed)
                    self._communicationHandler.write_motor('C', 'F', speed)
                    self._communicationHandler.write_motor('D', 'B', speed)
                else:
                    self._communicationHandler.write_motor('A', 'B', speed)
                    self._communicationHandler.write_motor('B', 'F', speed)
                    self._communicationHandler.write_motor('C', 'B', speed)
                    self._communicationHandler.write_motor('D', 'F', speed)

                if abs(diff) < 5:
                    self.brake()
                    return

    def turn_manual(self, direction: str, speed: int):
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
        # self._communicationHandler.write_motor('A', 'F', 255)
        # self._communicationHandler.write_motor('B', 'F', 255)
        # self._communicationHandler.write_motor('C', 'F', 255)
        # self._communicationHandler.write_motor('D', 'F', 255)
        # sleep(self._brake_delay)
        self._communicationHandler.write_motor('A', 'F', 0)
        self._communicationHandler.write_motor('B', 'F', 0)
        self._communicationHandler.write_motor('C', 'F', 0)
        self._communicationHandler.write_motor('D', 'F', 0)
