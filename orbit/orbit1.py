import pygame
import math

window = pygame.display.set_mode((500, 500))
run = True
biasx = 0
biasy = 0
speed_b = 0.2

def distance(obj_1_x, obj_1_y, obj_2_x, obj_2_y):
    dis = math.sqrt(((obj_2_x  - obj_1_x)**2) + ((obj_2_y  - obj_1_y)**2))
    return dis


pygame.init()
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        biasy += speed_b
    if keys[pygame.K_s]:
        biasy -= speed_b
    if keys[pygame.K_a]:
        biasx -= speed_b
    if keys[pygame.K_d]:
        biasx += speed_b
    window.fill((10, 10, 10))
    pygame.display.update()
pygame.quit()