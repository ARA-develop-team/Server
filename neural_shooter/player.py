"""class player"""

import math
import pygame


# pygame.font.init()


class OBJ:  # parent class for Player and Bot
    def __init__(self, position, color, hit_points, radius, view, name, color_info):
        self.name = name
        self.pos = position
        self.color = color
        self.HP = hit_points  # hit points
        self.player_radius = radius
        self.player_view = view
        self.color_info = color_info

    def draw(self, window, work_info_font, color=None):
        if color is None:
            color = self.color
        pygame.draw.circle(window, color, self.pos, self.player_radius, self.player_radius)
        hp_text = work_info_font.render(str(int(self.HP)), False, self.color_info)
        window.blit(hp_text, (self.pos[0] - 5, self.pos[1] + 10))


class Player(OBJ):

    def __init__(self, position, color, color_lines, speed, color_info, radius, view, name, hit_points):
        super().__init__(position, color, hit_points, radius, view, name, color_info)

        self.color_lines = color_lines
        self.speed = speed
        self.way_vector = None
        self.way_angle = None

    def __str__(self):
        return f"Player"

    def draw_lines(self, mouse, window, work_info_font):
        pygame.draw.circle(window, self.color_lines, self.pos, self.player_view, 1)

        if mouse:
            pygame.draw.line(window, self.color_lines, self.pos, mouse)
            self.way_vector = [mouse[0] - self.pos[0], mouse[1] - self.pos[1]]

        if self.way_angle:
            way_angle_degrees = math.degrees(self.way_angle)  # radians per degree
            angle_text = work_info_font.render(str(int(way_angle_degrees)), False, self.color_info)
            window.blit(angle_text, (20, 20))


class Bot(OBJ):
    def __init__(self, position, color, hit_points, radius, view, name, color_info, length_to_point):
        super().__init__(position, color, hit_points, radius, view, name, color_info)

        self.len = length_to_point         # length of lines
        self.delta = int(self.len / 1.41)       # diagonal of square
        self.view_point = []

    # def find_view_point(self):
    #     self.view_point.clear()
    #     self.view_point.append((self.pos[0] - self.len, self.pos[1]))
    #     self.view_point.append((self.pos[0] - self.delta, self.pos[1] - self.delta))
    #     self.view_point.append((self.pos[0], self.pos[1] - self.len))
    #     self.view_point.append((self.pos[0] + self.delta, self.pos[1] - self.delta))
    #     self.view_point.append((self.pos[0] + self.len, self.pos[1]))
    #     self.view_point.append((self.pos[0] + self.delta, self.pos[1] + self.delta))
    #     self.view_point.append((self.pos[0], self.pos[1] + self.len))
    #     self.view_point.append((self.pos[0] - self.delta, self.pos[1] + self.delta))

    def __str__(self):
        return f"Bot"


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
