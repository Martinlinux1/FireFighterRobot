import math

import errors


class FireFinder:
    @staticmethod
    def is_fire(temperatures, threshold: int, kernel_size):
        fire_positions = []
        for i in range(len(temperatures)):
            if temperatures[i] > threshold:
                kernel_start = 0
                kernel_end = 0
                if i - 15 < 0:
                    kernel_start = i - 15 - abs(i - 15)
                if i + 15 >= len(temperatures):
                    kernel_end = (i + 15) % (len(temperatures) - 1)
                kernel = temperatures[kernel_start:kernel_end]
                n_high_temperatures = 0
                for j in kernel:
                    if j > temperatures[i] - 5:
                        n_high_temperatures += 1

                if n_high_temperatures < kernel_size / 2:
                    fire_positions.append([i % 32, math.floor(i / 32), temperatures[i]])

        if fire_positions:
            return True, fire_positions
        else:
            return False, -1

    @staticmethod
    def max_fire(fire_coordinates):
        if fire_coordinates[0]:
            max_val = [0, 0, 0]
            for i in fire_coordinates[1]:
                if i[2] > max_val[2]:
                    max_val = i
            return max_val
        return [-1, -1, -1]

    @staticmethod
    def coordinates_to_angle(fire_coordinates):
        fire_angles = []
        if fire_coordinates[2] == -1:
            raise errors.NoFireDetectedError

        if isinstance(fire_coordinates, list):
            angle_horizontal = (fire_coordinates[0] * (120 / 32) - 120 / 2)

            angle_vertical = (fire_coordinates[1] * (75 / 24) - 15)

            fire_angles.append(angle_horizontal)
            fire_angles.append(angle_vertical)
            return fire_angles

