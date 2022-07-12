"""SHOOTER"""

import src
import pygame


class Shooter:
    def __init__(self):
        self.file = r"start.yml"  # file with data for config_parser
        self.data = None  # result of config_parser

        self.online = None  # type of game
        self.run = True
        self.player_name = None

        self.user_visual = None  # pygame code
        self.field = None  # object (class field)
        self.client = None  # object (class client), if self.online = True

        self.analysis = src.Analysis()
        self.clock = pygame.time.Clock()

        self.mouse_pos = []

    def start(self):
        #  PARSER
        #  get data from start.yml

        self.data = src.get_start_data(self.file)
        if not self.data:
            print('[NO DATA]')
            self.run = False
            self.exit()

        self.online = self.data['online']
        print("\033[35m{}".format(f"ONLINE: {self.online}"), "\033[0m".format(""))

        self.user_visual = pgCode.CPygame(self.data['screen_color'], self.data['screen_size'])
        if self.online:
            self.field = src.ServerField(self.data['start_vector'], self.data['screen_size'])
            self.client = src.Client(self.data['name'])
            self.player_name = self.data['name']
            self.playing_online()
        else:
            self.field = src.ServerField(self.data['start_vector'], self.data['screen_size'])
            self.user_visual.field = self.field
            self.field.player_dict[self.data['name']] = src.Player(self.data['start_point'], self.data['user_color'],
                                                                  self.data['color_lines'], self.data['user_speed'],
                                                                  self.data['color_info'],
                                                                  self.data['user_radius'][0],
                                                                  self.data['user_radius'][1],
                                                                  self.data['name'])
            self.player_name = self.data['name']
            self.playing()

    def playing(self):
        while self.run:
            # print fps
            self.clock.tick()
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

            event = self.input_data(self.field.player_dict[self.player_name])
            self.field.event_process(event)

            self.field.player_collision_processing(self.player_name)
            self.field.shooting_processing()
            self.field.bullets_processing()

            self.user_visual.draw_screen(self.field.player_dict, self.field.bullet_list,
                                         self.field.block_list, self.player_name)

    def playing_online(self):
        # connect to the server
        self.client.connect()

        self.analysis.launch()

        while self.run:

            # print fps
            self.clock.tick(30)
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

            # receive data_package from server
            self.field.player_dict, self.field.block_list, self.field.bullet_list = self.client.receive()

            event = self.input_data(self.field.player_dict[self.player_name])
            self.client.send(event)

            self.user_visual.draw_screen(self.field.player_dict, self.field.bullet_list,
                                         self.field.block_list, self.player_name)
            self.analysis.processing()

    def exit(self):  # for cancel threads
        if self.user_visual is not None:
            self.user_visual.run = False
        if self.online:
            self.client.signing_off()
            self.analysis.result()
        print("-----------END-----------")
        quit()

    def input_data(self, player):
        player_way_vector = player.way_vector
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
                self.exit()
                break

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
                self.user_visual.mouse_pos = self.mouse_pos

            if e.type == pygame.MOUSEBUTTONUP:
                # event shoot
                return [1, player.name]

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


if __name__ == "__main__":
    game = Shooter()

    print('----------START----------')
    game.start()

    quit()
