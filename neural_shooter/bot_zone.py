""" playground for testing bots """


import field
import pygame
import math
import config_parser as parser
import player


class Line:
    def __init__(self, length, delta):
        self.color = (250, 250, 250)
        self.len = length       # length of lines
        self.delta = delta

    def draw_line(self, num):
        pygame.draw.line(window, self.color, bot.pos, bot.view_point[num])


def start(file, sc_size=(500, 500), run=True):
    screen = pygame.display.set_mode(sc_size)
    pygame.display.set_caption('WELCOME')
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    f1 = pygame.font.Font(None, 40)
    f2 = pygame.font.Font(None, 25)
    text1 = f1.render('WELCOME TO THE BOT ZONE', True, (219, 215, 210))
    text2 = f2.render('--->   press SPACE to continue   <---', True, (219, 215, 210))
    text_size1 = text1.get_size()
    text_size2 = text2.get_size()
    if sc_size == (626, 626):
        screen.blit(text1, ((sc_size[0]/2) - (text_size1[0] / 2), 100))
        screen.blit(text2, ((sc_size[0]/2) - (text_size2[0] / 2), 570))

    else:
        screen.blit(text1, ((sc_size[0]/2) - (text_size1[0] / 2), (sc_size[1] / 2) - (text_size1[1] / 2) - 50))
        screen.blit(text2, ((sc_size[0]/2) - (text_size2[0] / 2), (sc_size[1] / 2) - (text_size2[1] / 2) + 50))

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
    field_for_game = field.CField(data['start_vector'], screen_size, data['user_radius'][0], data['bullet'], 'bot_zone')

    return data['screen_color'], field_for_game, bot_obj, data['bot_speed']


screen_size = (1000, 1000)
background = pygame.image.load('background.jpg')
if background.get_height() > 700 or background.get_width() > 700:
    background = pygame.transform.scale(background, (600, 600))

is_running = True
start_file = r"start.yml"
line_list = []

pygame.init()
work_info = pygame.font.SysFont('monospace', 16)

if __name__ == '__main__':
    screen_color, game_field, bot, bot_speed = (start(start_file, sc_size=background.get_size()))
    for _ in range(8):
        line_list.append(Line(bot.len, bot.delta))

    window = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('BOT ZONE')
    window.fill(screen_color)
    pygame.display.flip()
    clock = pygame.time.Clock()

    pp = game_field.field[0].width + game_field.field[0].height
    diagonal = int(game_field.field[0].width * 1.41)

    while is_running:

        window.fill(screen_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            bot.pos[0] -= bot_speed

        if keys[pygame.K_d]:
            bot.pos[0] += bot_speed

        if keys[pygame.K_w]:
            bot.pos[1] -= bot_speed

        if keys[pygame.K_s]:
            bot.pos[1] += bot_speed

        distance = []
        closest_block = []
        for block in game_field.field:
            length = math.sqrt((block.x - bot.pos[0])**2 + (block.y - bot.pos[1])**2)
            if length <= diagonal:
                closest_block.append((block.x, block.y, block.width, block.height))
                distance.append(length)

            # if length == distance[0]:
            #     closest_block.append((block.x, block.y, block.width, block.height))
            # elif length < distance[0]:
            #     closest_block.clear()
            #     distance.clear()
            #     closest_block.append((block.x, block.y, block.width, block.height))
            #     distance.append(length)

            block.draw(window)

        for i in range(len(closest_block)):
            distance.append(math.sqrt((closest_block[i][0] + closest_block[i][2] - bot.pos[0])**2
                                      + (closest_block[i][1] + closest_block[i][3] - bot.pos[1])**2))

        contact = False
        for diagonals in range(int(len(distance) / 2)):
            if pp >= (distance[diagonals] + distance[int(len(distance) / 2) + diagonals]):
                contact = True

        for point in closest_block:
            pygame.draw.line(window, (255, 255, 255), bot.pos, (point[0], point[1]), 2)
            pygame.draw.line(window, (255, 255, 255), bot.pos, (point[0] + point[2], point[1] + point[3]), 2)

        if contact:
            bot.draw(window, work_info, (255, 0, 0))
        else:
            bot.draw(window, work_info)

        # for x in range(len(line_list)):
        #     line_list[x].draw_line(x)

        pygame.display.update()
        clock.tick(100)

    pygame.quit()

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
