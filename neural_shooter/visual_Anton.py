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

    def draw_screen(self, player_dict, bullet_list, block_list, player_name):    # offline broken
        self.window.fill(self.screen_color)

        f1 = pygame.font.Font(None, 24)
        text1 = f1.render('EXIT', True, (219, 215, 210))
        self.window.blit(text1, (720, 220))

        for block in block_list:
            block.draw(self.window)

        for bullet in bullet_list:
            if distance_between_two_point(bullet.pos, player_dict[player_name].pos) < \
                    player_dict[player_name].player_view:
                pygame.draw.circle(self.window, (200, 200, 100), bullet.pos, 5, 5)

        if len(player_dict) != 0:           # drawing all players
            for player in player_dict.values():
                if player:
                    if distance_between_two_point(player.pos, player_dict[player_name].pos) < \
                            player_dict[player_name].player_view:
                        player.draw(self.window)

        player_dict[player_name].draw_lines(self.mouse_pos, self.window, self.work_info)     # for lines
        pygame.display.update()


def distance_between_two_point(a, b):
    distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return distance
