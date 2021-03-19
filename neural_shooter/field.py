"""PLAYING FIELD + logic of the game"""

import math


class CField:
    def __init__(self, start_vector):
        self.default_vector = start_vector

    def angle_of_track(self, way_vector):       # way  in degrees
        a, b = self.default_vector, way_vector

        scalar_products = (a[0] * b[0]) + (a[1] * b[1])
        module_a = math.sqrt((a[0]**2) + (a[1]**2))
        module_b = math.sqrt((b[0]**2) + (b[1]**2))

        try:
            alfa = math.acos(scalar_products / (module_a * module_b))

        except ZeroDivisionError:
            alfa = 90
        return alfa

    def vector(self, x1, y1, x2, y2, speed):  # считает направление между двумя объектами
        v_x_2 = x2 - x1
        v_y_2 = y2 - y1
        if v_x_2 != 0 or v_y_2 != 0:  # это нужно для того что бы в формула не делила на ноль
            v_x = int(v_x_2 / math.sqrt((v_x_2 ** 2 + v_y_2 ** 2) / speed ** 2))
            v_y = int(v_y_2 / math.sqrt((v_x_2 ** 2 + v_y_2 ** 2) / speed ** 2))
        else:
            v_x, v_y = 0, 0
        return v_x, v_y

    def distance(self, obj_1_x, obj_1_y, obj_2_x, obj_2_y):
        dis = math.sqrt(((obj_2_x - obj_1_x) ** 2) + ((obj_2_y - obj_1_y) ** 2))
        return dis

    def contact(self, obj_1_x, obj_1_y, radius_1, obj_2_x, obj_2_y, radius_2):
        dis = distance(obj_1_x, obj_1_y, obj_2_x, obj_2_y)
        if dis < radius_1 + radius_2:
            return True
        else:
            return False


if __name__ == "__main__":
    field = CField((1, 1))
    way = (-1, 1)
    result = field.angle_of_track(way)
    print(result)

