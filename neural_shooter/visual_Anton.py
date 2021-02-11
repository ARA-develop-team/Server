"""file for pygame"""

import pygame


class CPygame:
    def __init__(self, player, screen_color, screen_size):
        self.window = pygame.display.set_mode(screen_size)
        self.screen_color = screen_color
        self.run = True
        self.player = player
        self.mouse_pos = None

    def draw_screen(self, list_obj):
        self.window.fill(self.screen_color)
        if len(list_obj) != 0:
            for obj in list_obj:
                obj.draw(self.window)
        self.player.draw(self.mouse_pos)
        pygame.display.update()

    def input_data(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # client_f.signing_off()  # for online game
                self.run = False
                break

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.pos[0] -= self.player.speed

        if keys[pygame.K_d]:
            self.player.pos[0] += self.player.speed

        if keys[pygame.K_w]:
            self.player.pos[1] -= self.player.speed

        if keys[pygame.K_s]:
            self.player.pos[1] += self.player.speed





