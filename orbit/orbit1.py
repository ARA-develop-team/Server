import pygame

window = pygame.display.set_mode((500, 500))
run = True


pygame.init()
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    window.fill((10, 10, 10))
    pygame.display.update()

pygame.quit()