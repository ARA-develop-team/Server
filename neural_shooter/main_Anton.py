"""my version"""

import visual_Anton as pgCode
import player as pl
import config_parser as parser
import field
import client_f
import pygame
from analysis import CAnalysis


class CGame:
    def __init__(self):
        self.run = True
        self.file = r"start.yml"  # file with data for config_parser
        self.player = None  # player in this computer (obj class Player)
        self.user_visual = None  # pygame code
        self.data = None  # result of config_parser
        self.field = None  # object (class field)
        self.online = None  # type of game
        self.client = None  # object (class client), if self.online = True
        self.analysis = CAnalysis()

        self.block_list = []
        self.bullet_list = []
        self.player_dict = {}

        self.disconnected_key = []
        self.shoot = False
        self.mouse_pos = []

    def start(self):
        self.data = parser.getting_start_data(self.file)
        if not self.data:
            print('[NO DATA]')
            self.run = False
            self.exit()

        self.online = self.data['online']
        print("\033[35m{}".format(f"ONLINE: {self.online}"), "\033[0m".format(""))

        self.user_visual = pgCode.CPygame(self.player, self.data['screen_color'], self.data['screen_size'], None)
        if self.online:
            self.client = client_f.Client(self.data['name'])
            self.playing_online()
        else:
            self.field = field.CField(self.data['start_vector'], self.data['screen_size'], self.data['user_radius'][0],
                                      self.data['bullet'])
            self.player = pl.Player(self.data['start_point'], self.data['user_color'],
                                      self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                      self.data['user_radius'][0], self.data['user_radius'][1], self.data['name'])
            self.playing()

    def playing(self):
        self.player.window = self.user_visual.window
        self.analysis.launch()
        dict_obj = {self.data['name']: self.player}  # for player, bots and online players

        while self.user_visual.run:
            self.field.contact(self.player.pos[0], self.player.pos[1])
            self.user_visual.input_data()  # input in pygame
            if self.player.way_vector is not None:
                self.player.way_angle = self.field.angle_of_track(self.player.way_vector)
            self.user_visual.draw_screen(dict_obj)  # visual output
            self.field.bullets_action()
            self.analysis.processing()

        self.run = False
        self.exit()

    def playing_online(self):
        player, block_package_list = self.client.connect()
        self.player = pl.Player(player[2], player[4],
                                self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                self.data['user_radius'][0], self.data['user_radius'][1], player[1])
        self.player_dict[player[1]] = self.player

        for block in block_package_list:
            self.block_list.append(field.CBlock(*block))

        self.analysis.launch()

        while self.run:
            self.input_data()
            player_package_list, block_package_list, bullet_package_list = self.client.data_exchange(
                self.player.get_data_package(1))
            print(f'data {player_package_list, block_package_list, bullet_package_list}')

            for player_package in player_package_list:
                if player_package[0] == 3:
                    print('new player')
                    new_player = pl.Player(player_package[2], player_package[4],
                                           self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                           self.data['user_radius'][0], self.data['user_radius'][1], player_package[1])
                    self.player_dict[player_package[1]] = new_player
                else:
                    self.player_dict[player_package[1]].update_data(player_package)

            if block_package_list:
                for block_package in block_package_list:
                    for local_block in self.block_list:
                        if block_package[0] == local_block.number:
                            local_block.update_data(block_package)

            if len(bullet_package_list) > 0:
                for number in range(len(bullet_package_list)):
                    self.bullet_list[number].update_data(bullet_package_list[number])

            if self.player.way_vector is not None:
                self.player.way_angle = self.field.angle_of_track(self.player.way_vector)

            self.user_visual.draw_screen_online(self.player_dict, self.bullet_list, self.block_list)
            self.analysis.processing()

        self.run = False
        self.exit()

    def exit(self):  # for cancel threads
        if self.user_visual is not None:
            self.user_visual.run = False
        if self.online:
            self.client.signing_off()
        self.analysis.result()
        print("-----------END-----------")
        quit()

    def input_data(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.client.signing_off()  # for online game
                self.run = False
                break

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()

            if e.type == pygame.MOUSEBUTTONUP:
                self.shoot = True

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] and self.disconnected_key.count('a') == 0:
                self.player.pos[0] -= self.player.speed

            if keys[pygame.K_d] and self.disconnected_key.count('d') == 0:
                self.player.pos[0] += self.player.speed

            if keys[pygame.K_w] and self.disconnected_key.count('w') == 0:
                self.player.pos[1] -= self.player.speed

            if keys[pygame.K_s] and self.disconnected_key.count('s') == 0:
                self.player.pos[1] += self.player.speed


if __name__ == "__main__":
    game = CGame()

    print('----------START----------')
    game.start()

    quit()

    # def playing(self):
    #     self.user.window = self.user_visual.window
    #     self.analysis.launch()
    #     dict_obj = {self.data['name']: self.user}  # for player, bots and online players
    #
    #     while self.user_visual.run:
    #         self.field.contact(self.user.pos[0], self.user.pos[1])
    #         self.user_visual.input_data()  # input in pygame
    #         if self.user.way_vector is not None:
    #             self.user.way_angle = self.field.angle_of_track(self.user.way_vector)
    #         self.user_visual.draw_screen(dict_obj)  # visual output
    #         self.field.bullets_action()
    #         self.analysis.processing()
    #
    #     self.run = False
    #     self.exit()

# number_new_blocks = len(block_package_list) - len(self.block_list)
# for block in range(number_new_blocks):
#     self.block_list.append(field.CBlock(0, 0, 0, 0, 0))
#
# for number in range(len(block_package_list)):
#     self.block_list[number].update_data(block_package_list[number])
