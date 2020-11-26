import pygame

pygame.init()

screen_x = 500
screen_y = 500
window = pygame.display.set_mode((screen_x, screen_y))


class CPlayer:
    def __init__(self, p_name, p_x, p_y, p_color):
        self.name = p_name
        self.x = p_x
        self.y = p_y
        self.color = p_color
        self.speed = 10
        self.size = 10

    def draw(self):
        pygame.draw.circle(window, self.color, [self.x, self.y], self.size, self.size)

x = 0
y = 0
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
    if keys[pygame.K_s]:
    if keys[pygame.K_a]:
    if keys[pygame.K_d]:

    """отправка данных на сервер"""

    """принятие данных с сервера"""

    '''прорисовка'''
    window.fill((100, 100, 100))

    pygame.display.update()
pygame.quit()
