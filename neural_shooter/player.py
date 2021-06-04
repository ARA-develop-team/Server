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


class CBullet:
    def __init__(self, pos, radius, color, damage, speed, vector, owner):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.damage = damage
        self.speed = speed
        self.vector = vector
        self.owner = owner

    def motion(self):
        self.pos = [self.pos[0] + self.vector[0] * self.speed, self.pos[1] + self.vector[1] * self.speed]

    def draw(self, window):
        pygame.draw.circle(window, self.color, [int(self.pos[0]), int(self.pos[1])], self.radius, self.radius)

