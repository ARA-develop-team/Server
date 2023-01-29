"""SHOOTER"""

import src
import ui
import pygame


class Shooter:
    def __init__(self):
        self.file = r"start.yml"  # file with data for config_parser
        self.data = None  # data from config file

        self.online = None  # type of game
        self.player_name = None

        self.user_visual = None  # pygame code
        self.field = None  # object (class field)
        self.client = None  # object (class client), if self.online = True

        self.analysis = src.Analysis()
        self.clock = pygame.time.Clock()

        self.mouse_pos = [0, 0]

    def start(self):
        """
        Get data from config files.
        Set up online/offline game.
        """

        self.data = src.get_start_data(self.file)
        if not self.data:
            print('[NO DATA]')
            self.user_visual.run = False
            self.exit()

        self.online = self.data['online']
        print("\033[35m{}".format(f"ONLINE: {self.online}"), "\033[0m".format(""))

        self.user_visual = ui.CPygame(self.data['screen_color'], self.data['screen_size'], self.data['name'])
        self.field = src.ServerField(self.data['start_vector'], self.data['screen_size'])
        self.player_name = self.data['name']

        if self.online:
            self.client = src.Client(self.data['name'])
            self.playing_online()

        else:
            self.user_visual.field = self.field
            self.field.player_dict[self.data['name']] = src.Player(self.data['start_point'], self.data['user_color'],
                                                                   self.data['color_lines'], self.data['user_speed'],
                                                                   self.data['color_info'],
                                                                   self.data['user_radius'][0],
                                                                   self.data['user_radius'][1],
                                                                   self.data['name'])
            self.playing()

    def playing(self):
        while self.user_visual.run:
            # print fps
            self.clock.tick(30)
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

            self.user_visual.input_data()
            self.field.event_process(self.user_visual.status)

            self.field.player_collision_processing(self.player_name)
            self.field.shooting_processing()
            self.field.bullets_processing()

            self.user_visual.draw_screen(self.field.player_dict, self.field.bullet_list,
                                         self.field.block_list, self.player_name)

    def playing_online(self):
        # connect to the server
        self.client.connect()

        self.analysis.launch()

        while self.user_visual.run:
            # print fps
            self.clock.tick(30)
            pygame.display.set_caption(f"FPS: {self.clock.get_fps()}")

            # receive data_package from server
            self.field.player_dict, self.field.block_list, self.field.bullet_list = self.client.receive()

            self.user_visual.input_data()
            self.user_visual.status.collision = self.field.player_collision_processing(self.player_name)
            self.client.send(self.user_visual.status)

            self.user_visual.draw_screen(self.field.player_dict, self.field.bullet_list,
                                         self.field.block_list, self.player_name)
            self.analysis.processing()

        exit()

    def exit(self):  # cancel threads
        if self.user_visual is not None:
            self.user_visual.run = False

        if self.online:
            self.client.signing_off()
            self.analysis.result()

        print("-----------END-----------")
        quit()


if __name__ == "__main__":
    game = Shooter()

    print('----------START----------')
    game.start()
    print("-----------END-----------")

    quit()
