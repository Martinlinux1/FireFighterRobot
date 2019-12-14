import math


class FireFinder:
    @staticmethod
    def is_fire(temperatures, threshold: int):
        fire_positions = []
        for i in range(len(temperatures)):
            # print(self._temperatures[i])
            if i == 0:
                no_fire_pixels_around = True
            elif i < 32:
                no_fire_pixels_around = temperatures[i - 1] < threshold
            else:
                no_fire_pixels_around = temperatures[i - 1] < threshold and temperatures[i - 32] < \
                                        threshold and temperatures[i - 33] < threshold

            if temperatures[i] >= threshold and no_fire_pixels_around:
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

        if isinstance(fire_coordinates, list):
            angle_horizontal = (fire_coordinates[0] * (120 / 32) - 120 / 2)

            angle_vertical = (fire_coordinates[1] * (75 / 24) - 15)

            fire_angles.append(angle_horizontal)
            fire_angles.append(angle_vertical)
            return fire_angles

