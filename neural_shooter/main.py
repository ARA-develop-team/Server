"""main file of game"""

import socket
import pickle
import pygame
import client_f
import visual_py

player_pos = [100, 100]
speed = 1

pygame.init()

run = True
while run:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            client_f.signing_off()
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= speed

    if keys[pygame.K_d]:
        player_pos[0] += speed

    if keys[pygame.K_w]:
        player_pos[1] -= speed

    if keys[pygame.K_s]:
        player_pos[1] += speed

    list_obj = client_f.data_exchange(player_pos)
    visual_py.draw_screen(list_obj)

pygame.quit()
