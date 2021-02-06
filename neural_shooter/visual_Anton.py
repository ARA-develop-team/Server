"""file for pygame"""

import pygame


class CPygame:
    def __init__(self, player):
        self.window = pygame.display.set_mode((1000, 1000))
        self.screen_color = (0, 100, 200)
        self.run = True
        self.player = player

    def draw_screen(self, list_obj):
        self.window.fill(self.screen_color)
        if len(list_obj) != 0:
            for obj in list_obj:
                obj.draw(self.window)
        self.player.draw(self.window)
        pygame.display.update()

    def input_data(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # client_f.signing_off()  # for online game
                self.run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.pos[0] -= self.player.speed

        if keys[pygame.K_d]:
            self.player.pos[0] += self.player.speed

        if keys[pygame.K_w]:
            self.player.pos[1] -= self.player.speed

        if keys[pygame.K_s]:
            self.player.pos[1] += self.player.speed



