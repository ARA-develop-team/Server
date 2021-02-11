"""my version"""

import visual_Anton as pgCode
import player
import config_parser as parser
import field


class CGame:
    def __init__(self):
        self.run = True
        self.file = r"start.yml"
        self.user = None
        self.user_visual = None
        self.data = None
        self.field = None

    def start(self):
        self.data = parser.getting_start_data(self.file)
        if not self.data:
            self.run = False
            self.exit()

        self.user = player.Player(self.data['start_point'], self.data['user_color'],
                                  self.data['color_lines'], self.data['user_speed'], self.data['color_info'])
        self.user_visual = pgCode.CPygame(self.user, self.data['screen_color'], self.data['screen_size'])
        self.field = field.CField(self.data['start_vector'])
        self.playing()

    def playing(self):
        self.user.window = self.user_visual.window
        while self.user_visual.run:
            self.user_visual.input_data()
            if self.user.way_vector is not None:
                self.user.way_angle = self.field.angle_of_track(self.user.way_vector)
            self.user_visual.draw_screen([])  # change list in the future (online)
        self.run = False
        self.exit()

    def exit(self):  # for cancel threads
        if self.user_visual is not None:
            self.user_visual.run = False
        print("-----------END-----------")
        quit()


if __name__ == "__main__":
    game = CGame()
    print('----------START----------')
    game.start()

    quit()
