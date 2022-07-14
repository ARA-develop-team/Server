"""file for pygame"""

import pygame
import math

pygame.font.init()


class CPygame:
    def __init__(self, screen_color, screen_size):
        self.window = pygame.display.set_mode(screen_size)
        self.work_info = pygame.font.SysFont('monospace', 16)
        self.screen_color = screen_color
        self.mouse_pos = None
        self.run = True

    def draw_screen(self, player_dict, bullet_list, block_list, player_name):
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

    def input_data(self, player):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                break

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.mouse_pos = self.mouse_pos

            if e.type == pygame.MOUSEBUTTONUP:
                return [1, player.name]     # event shoot

        keys = pygame.key.get_pressed()

        player_pos_diff = [0, 0]
        if keys[pygame.K_a]:
            player_pos_diff[0] -= player.speed
            player.pos[0] -= player.speed

        if keys[pygame.K_d]:
            player_pos_diff[0] += player.speed
            player.pos[0] += player.speed

        if keys[pygame.K_w]:
            player_pos_diff[1] -= player.speed
            player.pos[1] -= player.speed

        if keys[pygame.K_s]:
            player_pos_diff[1] += player.speed
            player.pos[1] += player.speed

        player_way_vector = [self.mouse_pos[0] - player.pos[0], self.mouse_pos[1] - player.pos[1]]

        # event move
        return [0, player.name, player_pos_diff, player_way_vector]


def distance_between_two_point(a, b):
    distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return distance
