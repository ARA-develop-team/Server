"""PLAYING FIELD + logic of the game"""

import math
import pygame
# from test import test_img_load


def map_creation(screen_size):
    obj_list = []
    # blocks = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    #           [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]           # 0 - empty, 1 - wall
    blocks = [[0, 0, 1, 1],
              [0, 0, 0, 0],
              [1, 0, 0, 1],
              [1, 1, 1, 1]]
    # blocks = test_img_load()   # create map with picture
    sc_width, sc_height = screen_size[0], screen_size[1]

    obj_width = int(sc_width / len(blocks[0]))
    obj_height = int(sc_height / len(blocks))

    obj_y = 0
    for block in range(len(blocks)):
        obj_x = 0
        for kind in blocks[block]:
            if kind == 1:
                obj_list.append(CBlock(obj_x, obj_y, obj_width, obj_height, kind))
            obj_x += obj_width
        obj_y += obj_height

    return obj_list


class CBlock:
    def __init__(self, x, y, width, height, kind):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.kind = kind     # type

    def draw(self, window):
        pygame.draw.rect(window, (219, 215, 210), (self.x, self.y, self.width, self.height), 5)


class CField:
    def __init__(self, start_vector, screen_size):
        self.default_vector = start_vector
        self.field = map_creation(screen_size)

    def angle_of_track(self, way_vector):    # way  in radians
        a, b = self.default_vector, way_vector

        scalar_products = (a[0] * b[0]) + (a[1] * b[1])
        module_a = math.sqrt((a[0] ** 2) + (a[1] ** 2))
        module_b = math.sqrt((b[0] ** 2) + (b[1] ** 2))

        try:
            alfa = math.acos(scalar_products / (module_a * module_b))

        except ZeroDivisionError:
            alfa = 90
        return alfa

    def contact(self, player_x, player_y):     # add radius in future
        for block in self.field:
            if (block.x <= player_x <= block.x + block.width) and (block.y <= player_y <= block.y + block.height):
                pass
                # print(f"Touching with block № {self.field.index(block)}")


if __name__ == "__main__":
    # field = CField((1, 1))
    # way = (-1, 1)
    # result = field.angle_of_track(way)
    # print(result)
    obj_lst = map_creation((800, 800))






    # def vector(self, x1, y1, x2, y2, speed):  # calculates the direction between two objects
    #     v_x_2 = x2 - x1
    #     v_y_2 = y2 - y1
    #     if v_x_2 != 0 or v_y_2 != 0:  # cannot divide by zero (zero share)
    #         v_x = int(v_x_2 / math.sqrt((v_x_2 ** 2 + v_y_2 ** 2) / speed ** 2))
    #         v_y = int(v_y_2 / math.sqrt((v_x_2 ** 2 + v_y_2 ** 2) / speed ** 2))
    #     else:
    #         v_x, v_y = 0, 0
    #     return v_x, v_y

    # def distance(self, obj_1_x, obj_1_y, obj_2_x, obj_2_y):
    #     dis = math.sqrt(((obj_2_x - obj_1_x) ** 2) + ((obj_2_y - obj_1_y) ** 2))
    #     return dis
    #
    # def contact(self, obj_1_x, obj_1_y, radius_1, obj_2_x, obj_2_y, radius_2):
    #     dis = distance(obj_1_x, obj_1_y, obj_2_x, obj_2_y)
    #     if dis < radius_1 + radius_2:
    #         return True
    #     else:
    #         return False