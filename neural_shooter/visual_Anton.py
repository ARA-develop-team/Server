"""file for pygame"""

import pygame
import math

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

    def draw_screen_online(self, player_dict, bullet_package_list, block_list, player_name):
        self.window.fill(self.screen_color)

        f1 = pygame.font.Font(None, 24)
        text1 = f1.render('EXIT', True, (219, 215, 210))
        self.window.blit(text1, (720, 220))
        for block in block_list:
            block.draw(self.window)

        for bullet_package in bullet_package_list:
            if distance_between_two_point(bullet_package[2], player_dict[player_name].pos) < player_dict[player_name].player_view:
                self.draw_bullet_from_package(bullet_package)

        if len(player_dict) != 0:           # drawing all players
            for player in player_dict.values():
                if player:
                    if distance_between_two_point(player.pos, player_dict[player_name].pos) < player_dict[player_name].player_view:
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

    def draw_bullet_from_package(self, bullet_package):
        pygame.draw.circle(self.window, bullet_package[4], [int(bullet_package[2][0]), int(bullet_package[2][1])], bullet_package[3], bullet_package[3])


def distance_between_two_point(a, b):
    distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return distance
