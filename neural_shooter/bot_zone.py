""" playground for testing bots """
import time

import field
import pygame
import config_parser as parser
import player


def start(file, sc_size=(500, 500), run=True):
    screen = pygame.display.set_mode(sc_size)
    pygame.display.set_caption('WELCOME')
    screen.fill((0, 0, 0))

    f1 = pygame.font.Font(None, 40)
    f2 = pygame.font.Font(None, 25)
    text1 = f1.render('WELCOME TO THE BOT ZONE', True, (219, 215, 210))
    text2 = f2.render('--->   press SPACE to continue   <---', True, (219, 215, 210))
    text_size1 = text1.get_size()
    text_size2 = text2.get_size()
    screen.blit(text1, ((sc_size[0]/2) - (text_size1[0] / 2), (sc_size[1] / 2) - (text_size1[1] / 2) - 50))
    screen.blit(text2, ((sc_size[0]/2) - (text_size2[0] / 2), (sc_size[1] / 2) - (text_size2[1] / 2) + 50))

    pygame.display.flip()
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            run = False

    """start useful code"""

    data = parser.getting_start_data(file)
    bot_obj = player.Bot(data['bot_start_point'], data['bot_color'], data['bot_hit_points'],
                         data['bot_radius'][0], data['bot_radius'][1], 'bot', data['color_info'])
    field_for_game = field.CField(data['start_vector'], data['screen_size'], data['user_radius'][0], data['bullet'])

    return data['screen_color'], field_for_game, bot_obj


screen_size = (1000, 1000)
is_running = True
start_file = r"start.yml"
pygame.init()

if __name__ == '__main__':
    screen_color, game_field, bot = (start(start_file))
    window = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('BOT ZONE')
    window.fill(screen_color)
    pygame.display.flip()
    time.sleep(2)

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        for block in game_field.field:
            block.draw(window)

    pygame.quit()
