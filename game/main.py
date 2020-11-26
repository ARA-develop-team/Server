import pygame
import threading
from client_game import CClient

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


player = CPlayer()     # change in future
client_thread = threading.Thread(target=player.client, args=())
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    window.fill((100, 100, 100))

    pygame.display.update()
pygame.quit()
