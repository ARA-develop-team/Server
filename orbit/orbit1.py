import pygame
import random

window = pygame.display.set_mode((500, 500))
run = True


class Object:
    def __init__(self, x, y, color, radius, weight, impulse):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.weight = weight
        self.impulse = impulse

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, self.radius)


"""test code"""
planets = []
for a in range(0, 5):
    x = random.randint(5, 455)
    y = random.randint(5, 455)
    color = (255, 255, 255)
    radius = random.randint(5, 20)
    impulse = 0
    weight = 0
    planets.append(Object(x, y, color, radius, weight, impulse))
# end of test code

pygame.init()
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    window.fill((10, 10, 10))

    for planet in planets:
        planet.draw()

    pygame.display.update()

pygame.quit()
