"""my version"""

import visual_Anton as pgCode
import player
import config_parser as parser
import field
import client_f
from analysis import CAnalysis


class CGame:
    def __init__(self):
        self.run = True
        self.file = r"start.yml"        # file with data for config_parser
        self.user = None                # player in this computer (obj class Player)
        self.user_visual = None         # pygame code
        self.data = None                # result of config_parser
        self.field = None               # object (class field)
        self.online = None              # type of game
        self.client = None              # object (class client), if self.online = True
        self.analysis = CAnalysis()

    def start(self):
        self.data = parser.getting_start_data(self.file)
        if not self.data:
            self.run = False
            self.exit()

        self.online = self.data['online']
        print("\033[35m{}".format(f"ONLINE: {self.online}"), "\033[0m".format(""))

        self.user = player.Player(self.data['start_point'], self.data['user_color'],
                                  self.data['color_lines'], self.data['user_speed'], self.data['color_info'],
                                  self.data['user_radius'][0], self.data['user_radius'][1], self.data['name'])
        self.field = field.CField(self.data['start_vector'], self.data['screen_size'], self.data['user_radius'][0],
                                  self.data['bullet'])
        self.user_visual = pgCode.CPygame(self.user, self.data['screen_color'], self.data['screen_size'], self.field)
        self.field.input = self.user_visual
        if self.online:
            self.client = client_f.Client(self.data['name'])
            self.playing_online()
        else:
            self.playing()

    def playing(self):
        self.user.window = self.user_visual.window
        self.analysis.launch()
        dict_obj = {self.data['name']: self.user}    # for player, bots and online players

        while self.user_visual.run:
            self.field.contact(self.user.pos[0], self.user.pos[1])
            self.user_visual.input_data()       # input in pygame
            if self.user.way_vector is not None:
                self.user.way_angle = self.field.angle_of_track(self.user.way_vector)
            self.user_visual.draw_screen(dict_obj)  # visual output
            self.field.bullets_action()
            self.analysis.processing()

        self.run = False
        self.exit()

    def playing_online(self):
        dict_obj = self.client.connect()
        self.analysis.launch()

        while self.user_visual.run:
            self.field.contact(self.user.pos[0], self.user.pos[1])
            self.user_visual.input_data()
            dict_obj = self.client.data_exchange(self.user)
            if self.user.way_vector is not None:
                self.user.way_angle = self.field.angle_of_track(self.user.way_vector)
            self.user_visual.draw_screen(dict_obj)  # change list in the future (online)
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


if __name__ == "__main__":
    game = CGame()

    print('----------START----------')
    game.start()

    quit()
