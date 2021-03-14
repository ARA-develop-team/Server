"""main file of game"""

import pygame
import client_f
import visual_py

speed = 10

pygame.init()

client = client_f.Client('Roma1')

client.connect()

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            client.signing_off()
            break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.pos[0] -= speed

    if keys[pygame.K_d]:
        player.pos[0] += speed

    if keys[pygame.K_w]:
        player.pos[1] -= speed

    if keys[pygame.K_s]:
        player.pos[1] += speed

    list_obj = client.data_exchange(player)
    visual_py.draw_screen(list_obj)

pygame.quit()
