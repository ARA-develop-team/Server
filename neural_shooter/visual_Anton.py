"""file for pygame"""

import pygame

pygame.font.init()


class CPygame:
    def __init__(self, player, screen_color, screen_size, field):
        self.field = field
        self.window = pygame.display.set_mode(screen_size)
        self.work_info = pygame.font.SysFont('monospace', 16)
        self.screen_color = screen_color
        self.run = True
        self.player = player
        self.mouse_pos = None
        self.disconnected_key = []

    def draw_screen(self, list_obj):
        self.window.fill(self.screen_color)

        for block in self.field.field:
            block.draw(self.window)

        self.field.bullets_action(list_obj)     # function need ONLY LISTs!

        if len(list_obj) != 0:
            for obj in list_obj:
                obj.draw(self.window)

        # if len(list_obj) != 0:           # drawing all players  (with dictionary list)
        #     for obj in list_obj.values():
        #         if obj != 'None':
        #             obj.draw(self.window)

        self.player.draw_lines(self.mouse_pos, self.window, self.work_info)     # for lines
        pygame.display.update()

    def input_data(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # client_f.signing_off()  # for online game
                self.run = False
                break

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()

            if e.type == pygame.MOUSEBUTTONUP:
                self.field.shot_bullet_creation(self.player.way_vector, self.player.pos, self.player.name)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.disconnected_key.count('a') == 0:
            self.player.pos[0] -= self.player.speed

        if keys[pygame.K_d] and self.disconnected_key.count('d') == 0:
            self.player.pos[0] += self.player.speed

        if keys[pygame.K_w] and self.disconnected_key.count('w') == 0:
            self.player.pos[1] -= self.player.speed

        if keys[pygame.K_s] and self.disconnected_key.count('s') == 0:
            self.player.pos[1] += self.player.speed
