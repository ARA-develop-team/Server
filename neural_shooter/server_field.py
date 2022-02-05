
import field
import math
import queue
import time


class ServerField:
    def __init__(self, screen_size, radius):

        self.block_list, self.width, self.height = field.map_creation(screen_size)
        self.radius = radius  # radius of player
        self.player_dict = {}  # dict which contain list of class player and update list
        # each update list contain new information which client should take.  {player_name: [class pl, update list]}

        self.request_queue = queue.Queue()  # queue which contain data from players that server should process

        self.bullet_list = []
        self.bullet_num_list = []
        self.block_num_list = []
        self.bullet_counter = 0

    def main(self):
        # while not self.request_queue.empty():
        #     package = self.request_queue.get()
        #     print(package)
        #     self.player_dict[package[1]][0].update_data(package)
        #     # for block in self.block_list:
        #     #     self.contact_block_player(self.player_dict[package[1]][0], block)
        #
        #     for player_list in self.player_dict.values():
        #         # print(player_list)
        #         player_list[1].append(self.player_dict[package[1]][0].get_data_package(2))

        # for player in self.player_dict.keys():
        #     if self.player_dict[player][0].hp <= 0:
        #         self.player_dict.pop(player)
        #
        time.sleep(0.0001)
        for bullet in self.bullet_list:
            bullet.motion()
            for block in self.block_list:
                self.contact_bullet_block(bullet, block)
            for player in self.player_dict.keys():
                self.contact_bullet_player(bullet, self.player_dict[player][0])

    def contact_block_player(self, player, block):
        new_pos = player.pos
        right_side = player.pos[0] + self.radius - block.x
        up_side = player.pos[1] + self.radius - block.y
        left_side = block.x + block.width - player.pos[0] + self.radius
        down_side = block.y + block.width - player.pos[1] + self.radius

        if right_side > 0 and up_side > 0 and left_side > 0 and down_side > 0:  # if contact
            if right_side <= up_side and right_side <= down_side:
                print(f'right_side {player.pos[0] - right_side}')
                new_pos[0] = player.pos[0] - right_side
            elif left_side <= up_side and left_side <= down_side:
                print(f'left_side {player.pos[0] - left_side}')
                new_pos[0] = player.pos[0] + left_side
            elif up_side < down_side:
                print(f'up_side {player.pos[1] + up_side}')
                new_pos[1] = player.pos[1] - up_side
            else:
                print(f'down_side {player.pos[1] + down_side}')
                new_pos[1] = player.pos[1] + down_side

            player.pos = new_pos

    def contact_bullet_player(self, bullet, player):
        if bullet.owner != player.name:
            if distance_between_two_point(player.pos, [bullet.x, bullet.y]) < self.radius + bullet.radius:
                self.bullet_list.remove(bullet)
                self.bullet_num_list.remove(bullet.number)
                player.hp -= bullet.damage
                if player.hp <= 0:
                    player.pos = [500, 500]
                    player.hp = 100
                    self.player_dict[player.name][1].put(player.get_data_package(2))

    def contact_bullet_block(self, bullet, block):
        if (block.x - bullet.radius <= bullet.pos[0] <= block.x + block.width + bullet.radius) and \
                (block.y - bullet.radius <= bullet.pos[1] <= block.y + block.height + bullet.radius):
            if bullet in self.bullet_list:
                self.bullet_list.remove(bullet)

            if block.kind == 3:
                block.health -= bullet.damage
                if block.health <= 0:
                    self.block_list.remove(block)
                    self.block_num_list.remove(block.number)


def distance_between_two_point(a, b):
    distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return distance
