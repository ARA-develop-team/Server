"""class player"""

import math
import pygame
# pygame.font.init()


class Player(object):

    def __init__(self, position, color, color_lines, speed, color_info):
        self.pos = position
        self.color = color
        self.color_lines = color_lines
        self.color_info = color_info
        self.connection_number = False
        self.speed = speed
        # self.window = None
        self.way_vector = None
        self.way_angle = None
        # self.work_info = pygame.font.SysFont('monospace', 24)

    def draw(self, mouse, window, work_info_font):
        pygame.draw.circle(window, self.color, self.pos, 10, 10)
        pygame.draw.circle(window, self.color_lines, self.pos, 200, 1)

        if mouse:
            pygame.draw.line(window, self.color_lines, self.pos, mouse)
            self.way_vector = [mouse[0] - self.pos[0], mouse[1] - self.pos[1]]

        if self.way_angle:
            way_angle_degrees = math.degrees(self.way_angle)
            angle_text = work_info_font.render(str(way_angle_degrees), False, self.color_info)
            window.blit(angle_text, (20, 20))
