class CameraReader:
    def __init__(self, thermal_camera):
        self._thermal_camera = thermal_camera
        self._temperatures = self._thermal_camera.initializeFrame()

    def read_camera(self):
        sub_frame_0 = self._thermal_camera.initializeFrame()
        sub_frame_1 = self._thermal_camera.initializeFrame()

        self._thermal_camera.updateFrame(sub_frame_0)
        self._thermal_camera.updateFrame(sub_frame_1)

        for i in range(768):
            if i % 2 == 1:
                self._temperatures[i] = sub_frame_0[i]
            else:
                self._temperatures[i] = sub_frame_1[i]

        return self._temperatures

    def is_fire(self, threshold):
        fire_positions = []
        for i in range(768):
            if self._temperatures[i] >= threshold:
                fire_positions.append([i % 32, i % 24, self._temperatures[i]])
        if fire_positions:
            return True, fire_positions
        else:
            return False, -1

    def coordinates_to_angle(self, fire_coordinates):
        fire_angles = []

        if isinstance(fire_coordinates[0], list):
            for i in fire_coordinates:
                angle_horizontal = i[0] * (120 / 32) - 120 / 2

                angle_vertical = i[1] * (75 / 24) - 15

                fire_angles.append([angle_horizontal, angle_vertical])

            return fire_angles
        else:
            angle_horizontal = fire_coordinates[0] * (120 / 32) - 120 / 2

            angle_vertical = fire_coordinates[1] * (75 / 24) - 15

            fire_angles.append(angle_horizontal)
            fire_angles.append(angle_vertical)

            return fire_angles
