"""my version"""

import visual_Anton as pgCode
import player
import config_parser as parser


class CGame:
    def __init__(self):
        self.run = True
        self.file = r"start.yml"
        self.user = None
        self.user_visual = None
        self.data = None

    def start(self):
        self.data = parser.getting_start_data(self.file)
        if not self.data:
            self.run = False
            self.exit()

        self.user = player.Player(self.data['start_point'], self.data['user_color'],
                                  self.data['color_lines'], self.data['user_speed'])
        self.user_visual = pgCode.CPygame(self.user, self.data['screen_color'], self.data['screen_size'])
        self.playing()

    def playing(self):
        self.user.window = self.user_visual.window
        while self.user_visual.run:
            if not self.run:
                self.exit()

            self.user_visual.input_data()
            self.user_visual.draw_screen([])  # change list in the future (online)

    def exit(self):      # for cancel threads
        if self.user_visual is not None:
            self.user_visual.run = False
        print("----------EXIT----------")
        quit()


if __name__ == "__main__":
    game = CGame()
    game.start()

    quit()
