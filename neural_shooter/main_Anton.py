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
        self.player_name = None
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

        self.clock = pygame.time.Clock()

    def start(self):
        #  PARSER
        #  get data from start.yml

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
            self.player_name = self.data['name']
            self.playing_online()
        else:
            self.field = field.CField(self.data['start_vector'], self.data['screen_size'], self.data['user_radius'][0],
                                      self.data['bullet'])
            self.user_visual.field = self.field
            self.player = pl.Player(self.data['start_point'], self.data['user_color'],
                                    self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                    self.data['user_radius'][0], self.data['user_radius'][1], self.data['name'])
            self.playing()

    def playing(self):

        while self.run:
            # print fps
            self.clock.tick()
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

            self.input_data(self.player, self.field.block_list)

            self.user_visual.draw_screen(self.player)

    def playing_online(self):
        # connect to the server and get data (block_list and player_list)
        player_package_list, block_package_list = self.client.connect()
        for player_package in player_package_list:
            new_player = pl.Player(player_package[2], player_package[4],
                                   self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                   self.data['user_radius'][0], self.data['user_radius'][1], player_package[1])
            self.player_dict[player_package[1]] = new_player

        for block in block_package_list:
            self.block_list.append(field.CBlock(*block[1:]))

        self.analysis.launch()

        while self.run:
            # print fps
            self.clock.tick()
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

            # receive data_package from server
            updated_list, player_package_list, block_package_list, bullet_package_list = self.client.receive()

            # unpackage data
            for player_package in updated_list:
                if player_package[0] == 3:  # new player
                    print('new player')
                    new_player = pl.Player(player_package[2], player_package[4],
                                           self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                           self.data['user_radius'][0], self.data['user_radius'][1], player_package[1])
                    self.player_dict[player_package[1]] = new_player
                elif player_package[0] == 4:  # delete player
                    self.player_dict.pop(player_package[1])
                # else:  # update player
                #     print('updated')
                #     self.player_dict[player_package[1]].update_data(player_package)

            for player_package in player_package_list:
                self.player_dict[player_package[1]].update_data(player_package)

            for player_package in updated_list:
                if player_package[0] == 2:
                    self.player_dict[player_package[1]].update_data(player_package)

            for block_package in block_package_list:
                if block_package[0] == 3:  # new block
                    new_block = field.CBlock(*block_package[1:])
                    self.block_list.append(new_block)
                else:
                    delete_block = []

                    # find block in block_list
                    for block in self.block_list:
                        if block.number == block_package[1]:
                            if block_package[0] == 4:
                                delete_block.append(block.number)
                            else:
                                block.update_data(block_package)

                    for block in delete_block:
                        self.block_list.pop(block)

            for bullet_package in bullet_package_list:
                if bullet_package[0] == 3:
                    new_bullet = pl.CBullet(*bullet_package[1:])
                    self.bullet_list.append(new_bullet)
                else:
                    delete_bullet = []

                    # find bullet in bullet_list
                    for bullet in self.bullet_list:
                        if bullet.number == bullet_package[1]:
                            if bullet_package[0] == 4:
                                delete_bullet.append(bullet)
                            else:
                                bullet.update_data(bullet_package)

                    for bullet in delete_bullet:
                        self.bullet_list.remove(bullet)

            self.input_data(self.player_dict[self.player_name], self.block_list)

            self.client.send(self.player_dict[self.player_name].get_data_package(2))

            # if block_package_list:
            #     for block_package in block_package_list:
            #         for local_block in self.block_list:
            #             if block_package[0] == local_block.number:a
            #                 local_block.update_data(block_package)
            # for bullet_package in bullet_package_list:
            #     if bullet_package
            # if len(bullet_package_list) > 0:
            #     for number in range(len(bullet_package_list)):
            #         self.bullet_list[number].update_data(bullet_package_list[number])

            # if self.player.way_vector is not None:
            #     self.player.way_angle = self.field.angle_of_track(self.player.way_vector)

            self.user_visual.draw_screen_online(self.player_dict, self.bullet_list, self.block_list, self.player_name)
            self.analysis.processing()

    def exit(self):  # for cancel threads
        if self.user_visual is not None:
            self.user_visual.run = False
        if self.online:
            self.client.signing_off()
            self.analysis.result()
        print("-----------END-----------")
        quit()

    def input_data(self, player, block_list):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                self.exit()
                break

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()

            if e.type == pygame.MOUSEBUTTONUP:
                self.shoot = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.pos[0] -= player.speed
            for block in block_list:
                contact_block_player(player, block)

        if keys[pygame.K_d]:
            player.pos[0] += player.speed
            for block in block_list:
                contact_block_player(player, block)

        if keys[pygame.K_w]:
            player.pos[1] -= player.speed
            for block in block_list:
                contact_block_player(player, block)

        if keys[pygame.K_s]:
            player.pos[1] += player.speed
            for block in block_list:
                contact_block_player(player, block)


def contact_block_player(player, block):
    new_pos = player.pos
    right_side = player.pos[0] + player.player_radius - block.x
    up_side = player.pos[1] + player.player_radius - block.y
    left_side = block.x + block.width - player.pos[0] + player.player_radius
    down_side = block.y + block.width - player.pos[1] + player.player_radius

    if right_side > 0 and up_side > 0 and left_side > 0 and down_side > 0:  # if contact
        if right_side <= up_side and right_side <= down_side:
            new_pos[0] = player.pos[0] - right_side
        elif left_side <= up_side and left_side <= down_side:
            new_pos[0] = player.pos[0] + left_side
        elif up_side < down_side:
            new_pos[1] = player.pos[1] - up_side
        else:
            new_pos[1] = player.pos[1] + down_side

        player.pos = new_pos


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
