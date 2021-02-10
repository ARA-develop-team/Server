"""class player"""

import pygame


class Player(object):
    def __init__(self, pos, color, color_lines, speed):
        self.pos = pos
        self.color = color
        self.color_lines = color_lines
        self.connection_number = False
        self.speed = speed
        self.window = None

    def draw(self, mouse):
        pygame.draw.circle(self.window, self.color, self.pos, 10, 10)
        pygame.draw.circle(self.window, self.color_lines, self.pos, 200, 1)
        if mouse:
            pygame.draw.line(self.window, self.color_lines, self.pos, mouse)