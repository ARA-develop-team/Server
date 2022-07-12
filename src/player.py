"""class player"""

import math
import pygame


class Player(object):

    def __init__(self, position, color, color_lines, speed, color_info, radius, view, name):
        self.name = name
        self.speed = speed
        self.radius = radius
        self.player_view = view

        self.pos = position
        self.way_vector = None
        self.way_angle = None
        self.hp = 100
        self.shoot = False

        self.color = color
        self.color_lines = color_lines
        self.color_info = color_info

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius, self.radius)

    def draw_lines(self, mouse, window, work_info_font):
        pygame.draw.circle(window, self.color_lines, self.pos, self.player_view, 1)

        if mouse:
            pygame.draw.line(window, self.color_lines, self.pos, mouse)

        if self.way_angle:
            way_angle_degrees = math.degrees(self.way_angle)     # radians per degree
            angle_text = work_info_font.render(str(int(way_angle_degrees)), False, self.color_info)
            window.blit(angle_text, (20, 20))

    def get_data_package(self, type_package):
        # 1 - update package with shoot; 2 - update package; 3 - creation package

        if type_package == 1:
            if self.shoot:
                x = math.cos(self.way_angle)
                y = math.sin(self.way_angle)
                data_package = [type_package, self.name, self.pos, [x, y]]
                self.shoot = False
            else:
                data_package = [type_package, self.name, self.pos, None]
            return data_package

        if type_package == 2:
            data_package = [type_package, self.name, self.pos, self.hp]
            return data_package

        if type_package == 3:
            data_package = [type_package, self.name, self.pos, self.hp, self.color]
            return data_package

        if type_package == 4:
            data_package = [type_package, self.name]
            return data_package

        else:
            print('WRONG TYPE OF PACKAGE')


class CBullet:
    def __init__(self, number, pos, radius, color, damage, speed, vector, owner):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.damage = damage
        self.speed = speed
        self.vector = vector
        self.owner = owner
        self.number = number

    def motion(self):
        # print(self.pos, self.vector, self.speed,)
        self.pos = [self.pos[0] + self.vector[0] * self.speed, self.pos[1] + self.vector[1] * self.speed]

    def draw(self, window):
        pygame.draw.circle(window, self.color, [int(self.pos[0]), int(self.pos[1])], self.radius, self.radius)

    def get_data_package(self, type_package):
        if type_package == 3:
            data_package = [type_package, self.number, self.pos, self.radius, self.color, self.damage, self.speed, self.vector, self.owner]
            return data_package
        elif type_package == 1:
            data_package = [type_package, self.number, self.pos]
            return data_package
        else:
            print("WRONG TYPE")