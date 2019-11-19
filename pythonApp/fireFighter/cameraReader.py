import math


class CameraReader:
    def __init__(self, thermal_camera):
        """
        :type thermal_camera: USB2FIR
        """
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

    def is_fire(self, threshold: int):
        fire_positions = []
        for i in range(768):
            # print(self._temperatures[i])
            if i == 0:
                no_fire_pixels_around = True
            elif i < 32:
                no_fire_pixels_around = self._temperatures[i - 1] < threshold
            else:
                no_fire_pixels_around = self._temperatures[i - 1] < threshold and self._temperatures[i - 32] < \
                                        threshold and self._temperatures[i - 33] < threshold

            if self._temperatures[i] >= threshold and no_fire_pixels_around:
                print(i)
                fire_positions.append([i % 32, math.floor(i / 32), self._temperatures[i]])
        if fire_positions:
            return True, fire_positions
        else:
            return False, -1

    @staticmethod
    def max_fire(fire_coordinates):
        max_val = [0, 0, 0]
        for i in fire_coordinates[1]:
            print(i[2])
            if i[2] > max_val[2]:
                max_val = i
        return max_val

    @staticmethod
    def coordinates_to_angle(fire_coordinates):
        fire_angles = []

        if isinstance(fire_coordinates[0], list):
            for i in fire_coordinates:
                angle_horizontal = (i[0] * (120 / 32) - 120 / 2)

                angle_vertical = i[1] * (75 / 24) - 15

                fire_angles.append([angle_horizontal, angle_vertical])

            return fire_angles
        else:
            angle_horizontal = fire_coordinates[1][0][0] * (120 / 32) - 120 / 2

            angle_vertical = fire_coordinates[1][0][1] * (75 / 24) - 75 / 2

            fire_angles.append(angle_horizontal)
            fire_angles.append(angle_vertical)

            return fire_angles
