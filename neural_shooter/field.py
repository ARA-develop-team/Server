"""PLAYING FIELD + logic of the game"""

import math
import pygame
from player import CBullet


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
              [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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
                obj_list.append(CBlock(obj_x, obj_y, obj_width, obj_height, kind))
            elif kind == 3:
                obj_list.append(CBlock(obj_x, obj_y, obj_width, obj_height, kind, 100))  # 100 - health (temp)

            obj_x += obj_width
        obj_y += obj_height

    return obj_list, obj_width, obj_height


class CBlock:
    def __init__(self, x, y, width, height, kind, health=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.kind = kind  # type

    def draw(self, window):
        f1 = pygame.font.Font(None, 24)
        text1 = f1.render('EXIT', True, (219, 215, 210))
        window.blit(text1, (720, 220))

        if self.kind == 2:
            pygame.draw.rect(window, (0, 139, 139), (self.x, self.y, self.width, self.height), 5)
            self.kind = 1
        elif self.kind == 3:
            pygame.draw.rect(window, (227, 38, 54), (self.x, self.y, self.width, self.height), 5)
        else:
            pygame.draw.rect(window, (219, 215, 210), (self.x, self.y, self.width, self.height), 5)


class CField:
    def __init__(self, start_vector, screen_size, radius, bullet_data):
        self.default_vector = start_vector
        self.field, self.width, self.height = map_creation(screen_size)
        self.input = None  # visual.py
        self.radius = radius  # radius of player
        self.bullet_data = bullet_data
        self.bullet_list = []

    def angle_of_track(self, way_vector, default_vector=None, degrees=False):  # way in radians
        if default_vector:
            a, b = default_vector, way_vector
        else:
            a, b = self.default_vector, way_vector

        scalar_products = (a[0] * b[0]) + (a[1] * b[1])
        module_a = math.sqrt((a[0] ** 2) + (a[1] ** 2))
        module_b = math.sqrt((b[0] ** 2) + (b[1] ** 2))

        try:
            alfa = math.acos(scalar_products / (module_a * module_b))

        except ZeroDivisionError:
            alfa = 1.57079633

        if degrees:
            return math.degrees(alfa)
        else:
            return alfa

    def shot_bullet_creation(self, vector, pos, player_name):  # pos, radius, color, damage, speed, vector
        length_vector = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        unit_vector = [vector[0] / length_vector, vector[1] / length_vector]

        self.bullet_list.append(CBullet(pos, self.bullet_data[0], self.bullet_data[1], self.bullet_data[2],
                                        self.bullet_data[3], unit_vector, player_name))

    def bullets_action(self):
        if len(self.bullet_list) != 0:
            for bullet in self.bullet_list:
                bullet.motion()
                bullet.draw(self.input.window)

    def contact(self, player_x, player_y):  # add radius in future
        self.input.disconnected_key = []
        crossing_list = []           # crossing player with blocks

        for block in self.field:
            for bullet in self.bullet_list:  # bullet contact with blocks
                if (block.x - bullet.radius <= bullet.pos[0] <= block.x + block.width + bullet.radius) and \
                        (block.y - bullet.radius <= bullet.pos[1] <= block.y + block.height + bullet.radius):

                    if bullet.pos[0] < block.x + 2 or bullet.pos[0] > block.x + (block.width-2):
                        # left side    ° -> |     or right side  | <- °
                        angle = self.angle_of_track(bullet.vector, (0, 1))
                        bullet.vector = (bullet.vector[0] * (-1), bullet.vector[1])

                    elif bullet.pos[1] < block.y + 2 or bullet.pos[1] > block.y + (block.height-2):
                        # top side or bottom side    _°_
                        angle = self.angle_of_track(bullet.vector, (1, 0))
                        bullet.vector = (bullet.vector[0], bullet.vector[1] * (-1))

                    # self.bullet_list.remove(bullet)

                    if block.kind == 3:
                        block.health -= bullet.damage
                        if block.health <= 0:
                            self.field.remove(block)

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
                if self.width - 10 < crossing_list[0][0] < self.width and self.height - 10 < crossing_list[0][1] \
                        < self.height:  # [200, 200]
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
