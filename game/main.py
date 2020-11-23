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

class CPlayer:
    def __init__(self, p_name, p_x, p_y):
        self.name = p_name
        self.x = p_x
        self.y = p_y
        self.speed = 10
        self.size = 10
        self.color = (255, 168, 18)

