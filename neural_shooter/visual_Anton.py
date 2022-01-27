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

    def draw_screen(self, player):    # offline broken
        self.window.fill(self.screen_color)

        f1 = pygame.font.Font(None, 24)
        text1 = f1.render('EXIT', True, (219, 215, 210))
        self.window.blit(text1, (720, 220))

        for block in self.field.block_list:
            block.draw(self.window)

        # self.field.bullets_action()  # function need ONLY LISTs!

        # if len(list_obj) != 0:
        #     for obj in list_obj:
        #         obj.draw(self.window, self.work_info)

        player.draw(self.window)
        player.draw_lines(self.mouse_pos, self.window, self.work_info)  # for lines

        pygame.display.update()

    def draw_screen_online(self, player_dict, bullet_list, block_list, player_name):
        self.window.fill(self.screen_color)

        f1 = pygame.font.Font(None, 24)
        text1 = f1.render('EXIT', True, (219, 215, 210))
        self.window.blit(text1, (720, 220))
        for block in block_list:
            block.draw(self.window)

        for bullet in bullet_list:
            bullet.draw()

        if len(player_dict) != 0:           # drawing all players
            for player in player_dict.values():
                if player:
                    player.draw(self.window)

        player_dict[player_name].draw_lines(self.mouse_pos, self.window, self.work_info)     # for lines
        pygame.display.update()

    """Now this function moved to main.
    This version not functioned"""
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
