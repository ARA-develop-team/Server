"""class player"""

import math
import pygame
# pygame.font.init()


class Player(object):

    def __init__(self, position, color, color_lines, speed, color_info, radius, view, name):
        self.name = name
        self.pos = position
        self.color = color
        self.color_lines = color_lines
        self.color_info = color_info
        self.connection_number = False
        self.speed = speed
        self.way_vector = None
        self.way_angle = None
        self.player_radius = radius
        self.player_view = view
        self.disconnected_key = []
        self.hp = 100
        self.shoot = False

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.player_radius, self.player_radius)

    def draw_lines(self, mouse, window, work_info_font):
        pygame.draw.circle(window, self.color_lines, self.pos, self.player_view, 1)

        if mouse:
            pygame.draw.line(window, self.color_lines, self.pos, mouse)
            self.way_vector = [mouse[0] - self.pos[0], mouse[1] - self.pos[1]]

        if self.way_angle:
            way_angle_degrees = math.degrees(self.way_angle)     # radians per degree
            angle_text = work_info_font.render(str(int(way_angle_degrees)), False, self.color_info)
            window.blit(angle_text, (20, 20))

    def get_data_package(self, type_package):
        # 1 - update package with shoot; 2 - update package; 3 - creation package

        if type_package == 1:
            if self.shoot:
                data_package = [type_package, self.name, self.pos, self.way_vector]
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

        else:
            print('WRONG TYPE OF PACKAGE')

    def update_data(self, data_package):
        if data_package[0] == 3:
            self.name = data_package[1]
            self.pos = data_package[2]
            self.hp = data_package[3]
            self.color = data_package[4]
        elif data_package[1] == self.name:
            if data_package[0] == 1:
                self.pos = data_package[2]
                if self.way_vector:
                    self.way_vector = data_package[3]
            elif data_package[0] == 2:
                self.pos = data_package[2]
                self.hp = data_package[3]

            else:
                print(f'INCORRECT DATA PACKAGE: {data_package[0]}')
        else:
            print(f'WRONG NAME:  {self.name}, {data_package[1]}')


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
        print(self.pos, self.vector, self.speed,)
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

    def update_data(self, package):
        if package[0] == 1:
            self.pos = package[2]
        else:
            print("WRONG TYPE")
