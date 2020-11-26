import pygame
import random
import threading
import client_game

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


    def client(self):
        IP = 1  # input("IP: ")
        port = 1  # int(input("port: "))

        client = CClient(IP, port)
        client.connection_to_server()


x = 0
y = 0
r = random.randint(0,255)
g = random.randint(0,255)
b = random.randint(0,255)
color = (r, g, b)

player = CPlayer()     # change in future
client_thread = threading.Thread(target=player.client, args=())
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= 1
    if keys[pygame.K_s]:
        y += 1
    if keys[pygame.K_a]:
        x -= 1
    if keys[pygame.K_d]:
        x += 1

    """отправка данных на сервер"""

    """принятие данных с сервера"""

    '''прорисовка'''
    window.fill((100, 100, 100))

    pygame.display.update()
pygame.quit()
