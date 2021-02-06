"""class player"""

import pygame


class Player(object):
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.connection_number = False
        self.speed = 5

    def draw(self, window):
        pygame.draw.circle(window, (100, 0, 0), self.pos, 10, 10)
