import mathUtils


class MotorController:
    """Handles 4 motors with mecanum wheels motion."""

    def __init__(self, motors_handler, sensors_handler, encoders_handler, brake_delay):
        self._handler = motors_handler
        self._sensors_handler = sensors_handler
        self._encoders_handler = encoders_handler
        self._mathUtils = mathUtils.MathUtils()
        self._brake_delay = brake_delay

    """Moves the robot forward"""
    def forward(self, speed: int):
        self._handler.set_motor('A', 'F', speed)
        self._handler.set_motor('B', 'F', speed)
        self._handler.set_motor('C', 'F', speed)
        self._handler.set_motor('D', 'F', speed)
        self._handler.write_motors()

    def forward(self, speed: int, rotations: float):
        encoders_data = []

        while not encoders_data:
            encoders_data = self._encoders_handler.read()

        target_values = []

        for encoder in encoders_data:
            target_values.append(encoder + rotations)

        while True:
            encoders_data = []
            while not encoders_data:
                encoders_data = self._encoders_handler.read()

            diffs = []
            self.forward(speed)

            for i in range(len(encoders_data)):
                diffs = target_values[i] - encoders_data[i]

            if abs(diffs[0]) < 5:
                self.brake('A')
                return
            elif abs(diffs[1]) < 5:
                self.brake('B')
                return
            elif abs(diffs[2]) < 5:
                self.brake('C')
                return
            elif abs(diffs[3]) < 5:
                self.brake('D')
                return

    """Moves the robot backward."""
    def backward(self, speed: int):
        self._handler.set_motor('A', 'B', speed)
        self._handler.set_motor('B', 'B', speed)
        self._handler.set_motor('C', 'B', speed)
        self._handler.set_motor('D', 'B', speed)
        self._handler.write_motors()

    def backward(self, speed: int, rotations: float):
        encoders_data = []

        while not encoders_data:
            encoders_data = self._encoders_handler.read()

        target_values = []

        for encoder in encoders_data:
            target_values.append(encoder - rotations)

        while True:
            encoders_data = []
            while not encoders_data:
                encoders_data = self._encoders_handler.read()

            diffs = []
            self.backward(speed)

            for i in range(len(encoders_data)):
                diffs = target_values[i] - encoders_data[i]

            if abs(diffs[0]) < 5:
                self.brake('A')
                return
            elif abs(diffs[1]) < 5:
                self.brake('B')
                return
            elif abs(diffs[2]) < 5:
                self.brake('C')
                return
            elif abs(diffs[3]) < 5:
                self.brake('D')
                return

    def left(self, speed: int):
        self._handler.set_motor('A', 'B', speed)
        self._handler.set_motor('B', 'F', speed)
        self._handler.set_motor('C', 'B', speed)
        self._handler.set_motor('D', 'F', speed)
        self._handler.write_motors()

    def right(self, speed: int):
        self._handler.set_motor('A', 'F', speed)
        self._handler.set_motor('B', 'B', speed)
        self._handler.set_motor('C', 'F', speed)
        self._handler.set_motor('D', 'B', speed)
        self._handler.write_motors()

    """Slides the robot to a given angle."""
    def slide(self, angle: float, speed: int):
        if angle >= 0:
            if angle <= 45:
                bc_speed = int(self._mathUtils.valmap(angle, 45, 0, 0, speed))
                self._handler.set_motor('A', 'F', speed)
                self._handler.set_motor('B', 'F', bc_speed)
                self._handler.set_motor('C', 'F', bc_speed)
                self._handler.set_motor('D', 'F', speed)
            elif angle <= 90:
                bc_speed = int(self._mathUtils.valmap(angle, 45, 90, 0, speed))
                self._handler.set_motor('A', 'F', speed)
                self._handler.set_motor('B', 'B', bc_speed)
                self._handler.set_motor('C', 'B', bc_speed)
                self._handler.set_motor('D', 'F', speed)
            elif angle <= 135:
                ad_speed = int(self._mathUtils.valmap(angle, 135, 90, 0, speed))
                self._handler.set_motor('A', 'F', ad_speed)
                self._handler.set_motor('B', 'B', speed)
                self._handler.set_motor('C', 'B', speed)
                self._handler.set_motor('D', 'F', ad_speed)
            elif angle <= 180:
                bc_speed = int(self._mathUtils.valmap(angle, 135, 180, 0, speed))
                self._handler.set_motor('A', 'B', speed)
                self._handler.set_motor('B', 'B', bc_speed)
                self._handler.set_motor('C', 'B', bc_speed)
                self._handler.set_motor('D', 'B', speed)

        else:
            if angle >= -45:
                ad_speed = int(self._mathUtils.valmap(angle, -45, 0, 0, speed))
                self._handler.set_motor('A', 'F', ad_speed)
                self._handler.set_motor('B', 'F', speed)
                self._handler.set_motor('C', 'F', speed)
                self._handler.set_motor('D', 'F', ad_speed)
            elif angle >= -90:
                ad_speed = int(self._mathUtils.valmap(angle, -45, -90, 0, speed))
                self._handler.set_motor('A', 'B', ad_speed)
                self._handler.set_motor('B', 'F', speed)
                self._handler.set_motor('C', 'F', speed)
                self._handler.set_motor('D', 'B', ad_speed)
            elif angle >= -135:
                bc_speed = int(self._mathUtils.valmap(angle, -135, -90, 0, speed))
                self._handler.set_motor('A', 'B', speed)
                self._handler.set_motor('B', 'F', bc_speed)
                self._handler.set_motor('C', 'F', bc_speed)
                self._handler.set_motor('D', 'B', speed)
            elif angle >= -180:
                ad_speed = int(self._mathUtils.valmap(angle, -135, -180, 0, speed))
                self._handler.set_motor('A', 'B', ad_speed)
                self._handler.set_motor('B', 'B', speed)
                self._handler.set_motor('C', 'B', speed)
                self._handler.set_motor('D', 'B', ad_speed)

        self._handler.write_motors()

    """Turns the robot to a given angle"""
    def turn(self, angle: float, speed: int):
        sensors_data = []

        while not sensors_data:
            sensors_data = self._sensors_handler.read()

        robot_angle = sensors_data[2]

        target_angle = robot_angle + angle
        target_angle = target_angle % 360

        if target_angle < 0:
            target_angle = target_angle + 360

        while True:
            sensors_data = []
            while not sensors_data:
                sensors_data = self._sensors_handler.read()

            robot_angle = sensors_data[2]

            diff = target_angle - robot_angle
            direction = 180 - (diff + 360) % 360

            if direction > 0:
                self.right(speed)
            else:
                self.left(speed)

            if abs(diff) < 5:
                self.brake()
                return

    def point_to(self, angle, speed):
        sensors_data = []

        while not sensors_data:
            sensors_data = self._handler.get_sensors()

        robot_angle = sensors_data[2]
        diff = angle - robot_angle

        self.turn(diff, speed)

    def turn_manual(self, direction: str, speed: int):
        if direction == 'L':
            self.left(speed)
        elif direction == 'R':
            self.right(speed)

    """Stops all motors."""

    def brake(self):
        self._handler.set_motor('A', 'F', 0)
        self._handler.set_motor('B', 'F', 0)
        self._handler.set_motor('C', 'F', 0)
        self._handler.set_motor('D', 'F', 0)

        self._handler.write_motors()

    def brake(self, motor):
        self._handler.set_motor(motor, 'F', 0)

        self._handler.write_motors()
