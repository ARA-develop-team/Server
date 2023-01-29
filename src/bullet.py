import pygame
from src.config_parser import get_data


class Bullet:
    radius, color, damage, speed = get_data("start.yml", "bullet")

    def __init__(self, number, pos, vector, owner):
        self.pos = pos
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
            data_package = [type_package, self.number, self.pos, self.radius, self.color, self.damage, self.speed,
                            self.vector, self.owner]
            return data_package
        elif type_package == 1:
            data_package = [type_package, self.number, self.pos]
            return data_package
        else:
            print("WRONG TYPE")
