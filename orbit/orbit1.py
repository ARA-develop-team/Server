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
        self.G = 6.7 * (10 ** -11)  # G - gravitational constant

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, self.radius)

    def force_of_attraction(self, stranger_weight, distance):
        F = self.G * ((stranger_weight * self.weight) / (distance ** 2))  # F - force of attraction
        return F

    def motion(self):
        pass


"""test code"""
distance = 55.76 * (10**6)
planets = []
for a in range(0, 2):
    x = random.randint(5, 455)
    y = random.randint(5, 455)
    color = (255, 255, 255)
    radius = random.randint(5, 20)
    impulse = 0
    weight = 5.9726 * (10**24)
    planets.append(Object(x, y, color, radius, weight, impulse))
# end of test code


pygame.init()
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    window.fill((10, 10, 10))

    for planet in planets:
        # test code
        for second_planet in planets:
            if planet != second_planet:
                F = planet.force_of_attraction(second_planet.weight, distance)
                print(int(F))
        # end of test code
        planet.draw()

    pygame.display.update()

pygame.quit()
