"""file for pygame"""
import pygame

window = pygame.display.set_mode((500, 500))

def draw_screen(list_obj):
    window.fill((0, 100, 200))
    for obj in list_obj:
        pygame.draw.circle(window, (0, 0, 0), obj, 10, 10)
    pygame.display.update()
