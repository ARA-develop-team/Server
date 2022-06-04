import field
import math
import queue
import time
import player


class ServerField:
    def __init__(self, start_vector, screen_size, radius):
        self.default_vector = start_vector
        self.block_list, self.width, self.height = field.map_creation(screen_size)
        self.radius = radius  # radius of player
        self.player_dict = {}  # dict which contain list of class player and update list
        # each update list contain new information which client should take.  {player_name: [class pl, update list]}

        self.request_queue = queue.Queue()  # queue which contain data from players that server should process

        self.bullet_list = []
        self.bullet_num_list = []
        self.block_num_list = []
        self.bullet_counter = 0

        self.spawn_pos = [500, 500]

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

    def bullets_processing(self):
        for bullet in self.bullet_list:
            bullet.motion()
            for block in self.block_list:
                if contact_bullet_block(bullet, block):
                    if block.kind == 3:
                        block.health -= bullet.damage
                        if block.health <= 0:
                            self.block_list.remove(block)
                            # self.block_num_list.remove(block.number)
                    if bullet in self.bullet_list:
                        self.bullet_list.remove(bullet)

            for player in self.player_dict.keys():
                if contact_bullet_player(bullet, self.player_dict[player]):
                    player.hp -= bullet.damage
                    if player.hp <= 0:
                        player.pos = self.spawn_pos
                        player.hp = 100
                        # self.player_dict[player.name][1].put(player.get_data_package(2))
                    self.bullet_list.remove(bullet)

    def player_collision_processing(self, player_name):
        for block in self.block_list:
            ejection = contact_block_player(self.player_dict[player_name], block)
            self.player_dict[player_name].pos[0] += ejection[0]
            self.player_dict[player_name].pos[1] += ejection[1]

    def shooting_processing(self):
        for player in self.player_dict.keys():
            self.single_shooting_processing(player)

    def single_shooting_processing(self, player_name):
        if self.player_dict[player_name].shoot:
            self.shot_bullet_creation(player_name)
            self.player_dict[player_name].shoot = False

    def event_processing(self, event):
        if event[0] == 0:
            self.move_player(event[1], event[2])
        elif event[0] == 1:
            self.shot_bullet_creation(player_name)

    def angle_of_track(self, way_vector):  # way  in radians
        a, b = self.default_vector, way_vector

        scalar_products = (a[0] * b[0]) + (a[1] * b[1])
        module_a = math.sqrt((a[0] ** 2) + (a[1] ** 2))
        module_b = math.sqrt((b[0] ** 2) + (b[1] ** 2))

        try:
            alfa = math.acos(scalar_products / (module_a * module_b))

        except ZeroDivisionError:
            alfa = 90

        if way_vector[1] < 0:
            return -alfa
        return alfa

    def shot_bullet_creation(self, player_name):  # pos, radius, color, damage, speed, vector
        bullet_pos = self.player_dict[player_name].pos

        bullet_vector = [0, 0]
        bullet_vector[0] = math.cos(self.player_dict[player_name].way_angle)
        bullet_vector[1] = math.sin(self.player_dict[player_name].way_angle)

        self.bullet_list.append(player.CBullet(self.bullet_counter,
                                               bullet_pos, 5,
                                               (200, 200, 100), 10, 1,
                                               bullet_vector,
                                               player_name))

    def move_player(self, player_name, diff_pos):
        self.player_dict[player_name].pos[0] += diff_pos[0]
        self.player_dict[player_name].pos[1] += diff_pos[1]


def contact_block_player(player, block):
    ejection = [0, 0]
    right_side = player.pos[0] + player.radius - block.x
    up_side = player.pos[1] + player.radius - block.y
    left_side = block.x + block.width - player.pos[0] + player.radius
    down_side = block.y + block.width - player.pos[1] + player.radius

    if right_side > 0 and up_side > 0 and left_side > 0 and down_side > 0:  # if contact
        if right_side <= up_side and right_side <= down_side:
            ejection[0] = -right_side
        elif left_side <= up_side and left_side <= down_side:
            ejection[0] = left_side
        elif up_side < down_side:
            ejection[1] = -up_side
        else:
            ejection[1] = down_side
    return ejection


def contact_bullet_player(bullet, player):
    if bullet.owner != player.name:
        if distance_between_two_point(player.pos, bullet.pos) < player.radius + bullet.radius:
            return True
        return False


def contact_bullet_block(bullet, block):
    if (block.x - bullet.radius <= bullet.pos[0] <= block.x + block.width + bullet.radius) and \
            (block.y - bullet.radius <= bullet.pos[1] <= block.y + block.height + bullet.radius):
        return True
    return False


def distance_between_two_point(a, b):
    distance = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return distance
