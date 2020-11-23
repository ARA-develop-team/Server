import pygame

pygame.init()

screen_x = 500
screen_y = 500
window = pygame.display.set_mode((screen_x, screen_y))

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    window.fill((100, 100, 100))
    pygame.display.update()
pygame.quit()