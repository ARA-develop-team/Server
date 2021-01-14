import pygame
import math
import random

screen_x = 500
screen_y = 500
window = pygame.display.set_mode((screen_x, screen_y))
time_speed = 10

run = True

biasx = 0
biasy = 0
speed_b = 1

centre_x = int(screen_x / 2)
centre_y = int(screen_y / 2)
zoom = 1



def distance(obj_1_x, obj_1_y, obj_2_x, obj_2_y):
    dis = math.sqrt(((obj_2_x - obj_1_x) ** 2) + ((obj_2_y - obj_1_y) ** 2))
    return dis


def direction_between_two_point(x1, y1, x2, y2):
    return [x2 - x1, y1 - y2]


def combining_vectors(list_vector):
    comb_vector = [0, 0]
    for vector in list_vector:
        comb_vector[0] += vector[0]
        comb_vector[1] += vector[1]
    return comb_vector


def vector(x1, y1, x2, y2, speed):  # считает направление между двумя объектами
    v_x_2 = x2 - x1
    v_y_2 = y2 - y1
    if v_x_2 != 0 or v_y_2 != 0:  # это нужно для того что бы в формула не делила на ноль
        v_x = v_x_2 / math.sqrt((v_x_2 ** 2 + v_y_2 ** 2) / speed ** 2)
        v_y = v_y_2 / math.sqrt((v_x_2 ** 2 + v_y_2 ** 2) / speed ** 2)
    else:
        v_x, v_y = 0, 0
    return v_x, v_y


def classic_curvature_of_space():
    number = 0
    for obj in range(len(planets)):
        #print('obj = ' + str(obj))

        for obj_2 in range(obj + 1, len(planets)):
            #print('obj2 = ' + str(obj_2))
            #print(str(obj) + ' + ' + str(obj_2))

            length = distance(planets[obj].x, planets[obj].y, planets[obj_2].x, planets[obj_2].y)
            f = planets[obj].force_of_attraction(planets[obj_2].weight, length)
            dir = vector(planets[obj].x, planets[obj].y, planets[obj_2].x, planets[obj_2].y, 1)

            planets[obj].exert_force(f, dir)
            planets[obj_2].exert_force(f, [-dir[0], -dir[1]])


# print(combining_vectors([[2, 1], [1, 2], [0, 3]]))


class Camera:
    def __init__(self, x, y, zoom):
        self.x = x
        self.y = y
        self.zoom = zoom

    def show(self, list_object):
        for obj in list_object:
            if self.x - obj.radius < obj.x < self.x + obj.radius + (screen_x * self.zoom) and self.y - obj.radius < obj.y < self.y + obj.radius + (screen_y * self.zoom):
                obj.draw(self.x, self.y, self.zoom)

class Object:
    def __init__(self, x, y, color, radius, weight, start_impulse, direction):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.weight = weight
        self.speed = start_impulse
        self.dir = direction[0] * start_impulse, direction[1] * start_impulse
        self.G = 6.7 * (10 ** -11)  # G - gravitational constant

    def draw(self, bias_x, bias_y, zoom):
        # work with alternative coordinate system
        # alternative_x = self.x - centre_x + (bias_x * zoom)
        # alternative_y = self.y - centre_y + (bias_y * zoom)
        # zoom_x = alternative_x * zoom
        # zoom_y = alternative_y * zoom
        # if zoom_x == 0:
        #     zoom_x = random.randint(-1, 1)
        # if zoom_y == 0:
        #     zoom_y = random.randint(-1, 1)
        # comeback to real coordinate system
        # self.x = zoom_x + centre_x
        # self.y = zoom_y + centre_y

        # self.radius = self.radius * zoom
        pygame.draw.circle(window, self.color, (int(bias_x * zoom - self.x), int(bias_y * zoom - self.y)), int(self.radius * zoom), int(self.radius * zoom))

    def force_of_attraction(self, stranger_weight, distance):
        F = self.G * ((stranger_weight * self.weight) / (distance ** 2))  # F - force of attraction
        return F

    def exert_force(self, force, direction):
        dir = direction
        a = force / self.weight
        a /= 10000
        a /= 10000
        #print(a)
        #print([dir[0] * a, dir[1] * a])
        #print([self.dir[0], self.dir[1]])
        self.dir = combining_vectors([[dir[0] * a, dir[1] * a], [self.dir[0], self.dir[1]]])


    def motion(self):
        self.x += self.dir[0]
        self.y += self.dir[1]

"""test code"""
# distance = 55.76 * (10 ** 6)
planets = []
for a in range(0, 15
               ):
    x = random.randint(5, 455)
    y = random.randint(5, 455)
    color = (255, 255, 255)
    radius = random.randint(5, 20)
    impulse = 1
    weight = 5.9726 * (10 ** 1)
    planets.append(Object(x, y, color, radius, weight, impulse, [0, -1]))
# end of test code

camera = Camera(0, 0, 1)
planets.append(Object(0, 0, (0, 0, 255), 6.3, 6 * 10**20, 0, [0, 0]))
#planets.append(Object(150000, 0, (250, 200, 0), 696, 2 * 10**30, 50, [-1, 0]))
pygame.init()
f2 = pygame.font.SysFont('arial', 16)

while run:
    pygame.time.delay(time_speed)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.MOUSEMOTION:
            centre_x = e.pos[0]
            centre_y = e.pos[1]
        if e.type == pygame.MOUSEBUTTONDOWN:
            # zoom
            if e.button == 5:
                camera.zoom = camera.zoom / 2
                print(camera.zoom)
            if e.button == 4:
                camera.zoom = camera.zoom * 2
                print(camera.zoom)

    keys = pygame.key.get_pressed()
    # movement
    if keys[pygame.K_w]:
        camera.y -= speed_b
    if keys[pygame.K_s]:
        camera.y += speed_b
    if keys[pygame.K_a]:
        camera.x -= speed_b
    if keys[pygame.K_d]:
        camera.x += speed_b

    window.fill((10, 10, 10))

    # for planet in planets:
    #     # test code
    #     for second_planet in planets:
    #         if planet != second_planet:
    #             length = distance(planet.x, planet.y, second_planet.x, second_planet.y)
    #             # F = planet.force_of_attraction(second_planet.weight, length)
    #             # print(int(F))
    #     # end of test code
    #     planet.draw(biasx, biasy, zoom, centre_x, centre_y)
    camera.show(planets)
    for number in range(len(planets)):
        planets[number].motion()
    classic_curvature_of_space()

    text = f2.render(str(planets[1].dir), 1, (0, 180, 0))
    window.blit(text, (10, 20))
    text2 = f2.render(str(planets[0].dir), 1, (0, 180, 0))
    window.blit(text2, (10, 40))
    pygame.display.update()
    zoom = 1
    biasx = 0
    biasy = 0
pygame.quit()
