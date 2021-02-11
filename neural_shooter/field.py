"""PLAYING FIELD + logic of the game"""

import math


class CField:
    def __init__(self, start_vector):
        self.default_vector = start_vector

    def angle_of_track(self, way_vector):       # way  in degrees
        a, b = self.default_vector, way_vector

        scalar_products = (a[0] * b[0]) + (a[1] * b[1])
        module_a = math.sqrt((a[0]*a[0]) + (a[1]*a[1]))
        module_b = math.sqrt((b[0] * b[0]) + (b[1] * b[1]))

        try:
            alfa = math.acos(scalar_products / (module_a * module_b))

        except ZeroDivisionError:
            alfa = 90
        return alfa


if __name__ == "__main__":
    field = CField((1, 1))
    way = (-1, 1)
    result = field.angle_of_track(way)
    print(result)

