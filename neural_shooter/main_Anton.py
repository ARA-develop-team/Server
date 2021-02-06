"""my version"""

import visual_Anton as pgCode
import player


class CGame:
    def __init__(self):
        self.start_point = [200, 200]
        self.color = (200, 100, 0)
        self.user = None
        self.user_visual = None

    def start(self):
        self.user = player.Player(self.start_point, self.color)
        self.user_visual = pgCode.CPygame(self.user)
        self.playing()

    def playing(self):
        while self.user_visual.run:
            self.user_visual.input_data()
            self.user_visual.draw_screen([])  # change list in the future (online)


if __name__ == "__main__":
    game = CGame()
    game.start()

    quit()
