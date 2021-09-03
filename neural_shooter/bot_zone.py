""" playground for testing bots """

import field
import pygame
import math
import config_parser as parser
import player
import random


class BotZone:
    def __init__(self):
        self.photo = f'Roma.jpg'
        self.screen_size = (1000, 1000)
        self.background = pygame.image.load(self.photo)
        self.input = True

        if self.photo == f'Roma.jpg':
            self.background = pygame.transform.scale(self.background, (701, 701))
        elif self.background.get_height() > 700 or self.background.get_width() > 700:
            self.background = pygame.transform.scale(self.background, (700, 700))

        self.is_running = True
        self.start_file = r"start.yml"
        self.line_list = []

        pygame.init()
        self.work_info = pygame.font.SysFont('monospace', 16)

        self.screen_color, self.game_field, self.bot, self.bot_speed = \
            self.preparation(self.start_file, sc_size=self.background.get_size())

        self.window = pygame.display.set_mode(self.screen_size)

        for _ in range(8):
            self.line_list.append(Line(self.bot.len, self.bot.delta, self.window))

        pygame.display.set_caption('BOT ZONE')
        self.window.fill(self.screen_color)
        pygame.display.flip()
        self.clock = pygame.time.Clock()

        self.pp = self.game_field.field[0].width + self.game_field.field[0].height
        self.diagonal = int(self.game_field.field[0].width * 1.41)

    def preparation(self, file, sc_size=(500, 500), run=True):
        screen = pygame.display.set_mode(sc_size)
        pygame.display.set_caption('WELCOME')
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))

        if sc_size == (701, 701):
            color = (0, 0, 0)
        else:
            color = (219, 215, 210)

        error_list = []
        for _ in range(0, 45):
            num = random.randint(1000, 9999)
            error_list.append(pygame.font.Font(None, 15).render(f'ERROR {num}', True, color))

        f1 = pygame.font.Font(None, 40)
        f2 = pygame.font.Font(None, 25)
        text1 = f1.render('WELCOME TO THE BOT ZONE', True, color)
        text2 = f2.render('--->   press SPACE to continue   <---', True, color)
        text_size1 = text1.get_size()
        text_size2 = text2.get_size()
        if sc_size == (626, 626):
            screen.blit(text1, ((sc_size[0] / 2) - (text_size1[0] / 2), 100))
            screen.blit(text2, ((sc_size[0] / 2) - (text_size2[0] / 2), 570))

        elif sc_size == (701, 701):
            for err in range(0, len(error_list) - 1):
                screen.blit(error_list[err], (10, 10 + (err * error_list[err].get_size()[1] + 5)))

            screen.blit(text1, ((sc_size[0] / 2) - (text_size1[0] / 2), 100))
            screen.blit(text2, ((sc_size[0] / 2) - (text_size2[0] / 2), 150))

        else:
            screen.blit(text1, ((sc_size[0] / 2) - (text_size1[0] / 2), (sc_size[1] / 2) - (text_size1[1] / 2) - 50))
            screen.blit(text2, ((sc_size[0] / 2) - (text_size2[0] / 2), (sc_size[1] / 2) - (text_size2[1] / 2) + 50))

        pygame.display.flip()
        while run:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                    quit()

            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE]:
                run = False

        """start useful code"""

        data = parser.getting_start_data(file)
        bot_obj = player.Bot(data['bot_start_point'], data['bot_color'], data['bot_hit_points'],
                             data['bot_radius'][0], data['bot_radius'][1], 'bot', data['color_info'],
                             data['bot_length_to_point'])
        field_for_game = field.CField(data['start_vector'], self.screen_size, data['user_radius'][0], data['bullet'],
                                      'bot_zone')

        return data['screen_color'], field_for_game, bot_obj, data['bot_speed']

    def run(self):
        while self.is_running:
            self.window.fill(self.screen_color)

            if self.input:
                self.pygame_input()

            distance = []
            closest_block = []
            for block in self.game_field.field:
                length = math.sqrt((block.x - self.bot.pos[0]) ** 2 + (block.y - self.bot.pos[1]) ** 2)
                if length <= self.diagonal:
                    closest_block.append((block.x, block.y, block.width, block.height))
                    distance.append(length)

                # if length == distance[0]:
                #     closest_block.append((block.x, block.y, block.width, block.height))
                # elif length < distance[0]:
                #     closest_block.clear()
                #     distance.clear()
                #     closest_block.append((block.x, block.y, block.width, block.height))
                #     distance.append(length)

                block.draw(self.window)

            for i in range(len(closest_block)):
                distance.append(math.sqrt((closest_block[i][0] + closest_block[i][2] - self.bot.pos[0]) ** 2
                                          + (closest_block[i][1] + closest_block[i][3] - self.bot.pos[1]) ** 2))

            contact = False
            for diagonals in range(int(len(distance) / 2)):
                if self.pp >= (distance[diagonals] + distance[int(len(distance) / 2) + diagonals]):
                    contact = True

            for point in closest_block:
                pygame.draw.line(self.window, (255, 255, 255), self.bot.pos, (point[0], point[1]), 2)
                pygame.draw.line(self.window, (255, 255, 255), self.bot.pos, (point[0] + point[2], point[1] + point[3]),
                                 2)

            if contact:
                self.bot.draw(self.window, self.work_info, (255, 0, 0))
            else:
                self.bot.draw(self.window, self.work_info)

            # for x in range(len(line_list)):
            #     line_list[x].draw_line(x)

            pygame.display.update()
            self.clock.tick(100)

        pygame.quit()

    def pygame_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.bot.pos[0] -= self.bot_speed

        if keys[pygame.K_d]:
            self.bot.pos[0] += self.bot_speed

        if keys[pygame.K_w]:
            self.bot.pos[1] -= self.bot_speed

        if keys[pygame.K_s]:
            self.bot.pos[1] += self.bot_speed


class Line:
    def __init__(self, length, delta, window):
        self.color = (250, 250, 250)
        self.len = length  # length of lines
        self.delta = delta
        self.window = window

    def draw_line(self, num, bot):
        pygame.draw.line(self.window, self.color, bot.pos, bot.view_point[num])


if __name__ == '__main__':
    bot_zone = BotZone()
    bot_zone.run()


# # /
# photo = f'Roma.jpg'
# screen_size = (1000, 1000)
# background = pygame.image.load(photo)
#
#
# if photo == f'Roma.jpg':
#     background = pygame.transform.scale(background, (701, 701))
# elif background.get_height() > 700 or background.get_width() > 700:
#     background = pygame.transform.scale(background, (700, 700))
#
# is_running = True
# start_file = r"start.yml"
# line_list = []
# # \

# self.

    # for rect in game_field.field:
    #     rect_list.append(pygame.Rect(rect.x, rect.y, rect.width, rect.height))
    #
    # print(rect_list)
# for rect in rect_list:
#     contact = pygame.Rect.collidepoint(rect, bot.pos[0], bot.pos[1])
#     if contact == 1:
#         print('contact')
#     pygame.draw.rect(window, (250, 0, 0), rect, 6)

# if num == 0:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0] - self.len, bot.pos[1]))  # -b
# elif num == 1:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0] - self.delta, bot.pos[1] - self.delta))  # \
# elif num == 2:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0], bot.pos[1] - self.len))  # |
# elif num == 3:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0] + self.delta, bot.pos[1] - self.delta))  # /
# elif num == 4:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0] + self.len, bot.pos[1]))  # b-
# elif num == 5:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0] + self.delta, bot.pos[1] + self.delta))  # \
# elif num == 6:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0], bot.pos[1] + self.len))  # |
# elif num == 7:
#     pygame.draw.line(window, self.color, bot.pos, (bot.pos[0] - self.delta, bot.pos[1] + self.delta))  # /
