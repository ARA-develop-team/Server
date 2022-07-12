"""PLAYING FIELD + logic of the game"""

import math
import pygame
from bullet import Bullet


# from test import test_img_load


def map_creation(screen_size):
    obj_list = []
    # 0 - empty; 1 - wall; 2 - blue wall; 3 - destructible wall;
    blocks = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [1, 0, 1, 3, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    # blocks = [[1, 1, 1, 1],
    #           [1, 0, 0, 1],
    #           [1, 0, 0, 1],
    #           [1, 1, 1, 1]]
    # blocks = test_img_load()   # create map with picture
    sc_width, sc_height = screen_size[0], screen_size[1]

    obj_width = int(sc_width / len(blocks[0]))
    obj_height = int(sc_height / len(blocks))

    obj_y = 0
    for block in range(len(blocks)):
        obj_x = 0
        for kind in blocks[block]:
            if kind == 1 or kind == 2:
                obj_list.append(Block(block, obj_x, obj_y, obj_width, obj_height, kind))
            elif kind == 3:
                obj_list.append(Block(block, obj_x, obj_y, obj_width, obj_height, kind, 100))  # 100 - health (temp)
            obj_x += obj_width
        obj_y += obj_height

    # for obj in obj_list:
    #     print(obj_list.index(obj), obj.x, obj.y, obj.kind)
    print('map created')
    return obj_list, obj_width, obj_height


class Block:
    def __init__(self, number, x, y, width, height, kind, health=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.kind = kind  # type
        self.number = number

    def draw(self, window):
        if self.kind == 2:
            pygame.draw.rect(window, (0, 139, 139), (self.x, self.y, self.width, self.height), 5)
            self.kind = 1
        elif self.kind == 3:
            pygame.draw.rect(window, (227, 38, 54), (self.x, self.y, self.width, self.height), 5)
        else:
            pygame.draw.rect(window, (219, 215, 210), (self.x, self.y, self.width, self.height), 5)

    def get_data_package(self, type_package):
        # 1 - update package; 3 - creation package

        if type_package == 3:  # creation
            data_package = [type_package, self.number, self.x, self.y, self.width, self.height, self.kind, self.health]
            return data_package

        elif type_package == 1:  # update package
            data_package = [type_package, self.number, self.kind]
            return data_package

        else:
            print('WRONG TYPE OF PACKAGE')

    def update_data(self, package):
        if package[0] == 1:
            self.kind = package[1]  # = package[0], package[1], package[2]


class Field:
    def __init__(self, start_vector, screen_size, radius, bullet_data):
        self.default_vector = start_vector
        self.block_list, self.width, self.height = map_creation(screen_size)
        self.input = None  # visual.py
        self.radius = radius  # radius of player
        self.bullet_data = bullet_data

        self.bullet_list = []
        self.player_dict = []

    def angle_of_track(self, way_vector):  # way  in radians
        a, b = self.default_vector, way_vector

        scalar_products = (a[0] * b[0]) + (a[1] * b[1])
        module_a = math.sqrt((a[0] ** 2) + (a[1] ** 2))
        module_b = math.sqrt((b[0] ** 2) + (b[1] ** 2))

        try:
            alfa = math.acos(scalar_products / (module_a * module_b))

        except ZeroDivisionError:
            alfa = 90

        if way_vector[1] < 0:
            return -alfa
        return alfa

    def shot_bullet_creation(self, vector, pos, player_name):  # pos, radius, color, damage, speed, vector
        length_vector = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        unit_vector = [vector[0] / length_vector, vector[1] / length_vector]

        self.bullet_list.append(Bullet(pos, self.bullet_data[0], self.bullet_data[1], self.bullet_data[2],
                                       self.bullet_data[3], unit_vector, player_name))

    def bullets_action(self):
        if len(self.bullet_list) != 0:
            for bullet in self.bullet_list:
                bullet.motion()
                bullet.draw(self.input.window)

    def contact(self, player_x, player_y):  # add radius in future
        self.input.disconnected_key = []
        crossing_list = []

        for block in self.block_list:
            for bullet in self.bullet_list:  # bullet contact with blocks
                if (block.x - bullet.radius <= bullet.pos[0] <= block.x + block.width + bullet.radius) and \
                        (block.y - bullet.radius <= bullet.pos[1] <= block.y + block.height + bullet.radius):
                    self.bullet_list.remove(bullet)

                    if block.kind == 3:
                        block.health -= bullet.damage
                        if block.health <= 0:
                            self.block_list.remove(block)

            # start player & blocks contact
            if (block.x - self.radius <= player_x <= block.x + block.width + self.radius) and \
                    (block.y - self.radius <= player_y <= block.y + block.height + self.radius):
                if block.kind != 3:
                    block.kind = 2
                crossing_x, crossing_y = player_x - block.x, player_y - block.y  # pos of crossing block with player
                crossing_list.append([crossing_x, crossing_y])

                if crossing_x == 0 and crossing_y != 0 and crossing_y != self.height:
                    self.input.disconnected_key.append('d')
                if crossing_x == self.width and crossing_y != 0 and crossing_y != self.height:
                    self.input.disconnected_key.append('a')
                if crossing_y == 0 and crossing_x != 0 and crossing_x != self.width:
                    self.input.disconnected_key.append('s')
                if crossing_y == self.height and crossing_x != 0 and crossing_x != self.width:
                    self.input.disconnected_key.append('w')

        array_length = len(crossing_list)
        if array_length != 0 and len(self.input.disconnected_key) == 0:

            if array_length == 1:
                if 0 < crossing_list[0][0] < 10 and 0 < crossing_list[0][1] < 10:  # [0, 0]
                    self.input.disconnected_key.append('s')
                    self.input.disconnected_key.append('d')
                if self.width - 10 < crossing_list[0][0] < self.width and 0 < crossing_list[0][1] < 10:  # [200, 0]
                    self.input.disconnected_key.append('a')
                    self.input.disconnected_key.append('s')
                if self.width - 10 < crossing_list[0][0] < self.width and self.height - 10 < crossing_list[0][1] < \
                        self.height:  # [200, 200]
                    self.input.disconnected_key.append('w')
                    self.input.disconnected_key.append('a')
                if 0 < crossing_list[0][0] < 10 and self.height - 10 < crossing_list[0][1] < self.height:  # [0, 200]
                    self.input.disconnected_key.append('w')
                    self.input.disconnected_key.append('d')

            if array_length == 2:

                if crossing_list[0][0] + crossing_list[1][0] == 0:  # x1 + x2
                    self.input.disconnected_key.append('d')
                if crossing_list[0][0] + crossing_list[1][0] == self.width * 2:  # x1 + x2
                    self.input.disconnected_key.append('a')
                if crossing_list[0][1] + crossing_list[1][1] == 0:  # y1 + y2
                    self.input.disconnected_key.append('s')
                if crossing_list[0][1] + crossing_list[1][1] == self.height * 2:  # y1 + y2
                    self.input.disconnected_key.append('w')

        if array_length == 3:
            sum_x = crossing_list[0][0] + crossing_list[1][0] + crossing_list[2][0]
            sum_y = crossing_list[0][1] + crossing_list[1][1] + crossing_list[2][1]

            if sum_x == self.width and sum_y == self.height:
                self.input.disconnected_key.append('s')
                self.input.disconnected_key.append('d')

            if sum_x == self.width * 2 and sum_y == self.height:
                self.input.disconnected_key.append('s')
                self.input.disconnected_key.append('a')

            if sum_x == self.width * 2 and sum_y == self.height * 2:
                self.input.disconnected_key.append('w')
                self.input.disconnected_key.append('a')

            if sum_x == self.width and sum_y == self.height * 2:
                self.input.disconnected_key.append('w')
                self.input.disconnected_key.append('d')


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
