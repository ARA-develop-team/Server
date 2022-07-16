import src.field as field
from src.bullet import Bullet

import math


class ServerField:
    def __init__(self, start_vector, screen_size):
        self.player_dict = {}
        self.block_list, self.width, self.height = field.map_creation(screen_size)
        self.bullet_list = []

        self.bullet_counter = 0
        self.default_vector = start_vector
        self.spawn_pos = [500, 500]
        self.bullet_speed = 1

    def bullets_processing(self):
        for bullet in self.bullet_list:
            bullet.motion()
            for block in self.block_list:
                if contact_bullet_block(bullet, block):
                    if block.kind == 3:
                        block.health -= bullet.damage
                        if block.health <= 0:
                            self.block_list.remove(block)
                    if bullet in self.bullet_list:
                        self.bullet_list.remove(bullet)

            for player in self.player_dict.keys():
                if contact_bullet_player(bullet, self.player_dict[player]):
                    player.hp -= bullet.damage
                    if player.hp <= 0:
                        player.pos = self.spawn_pos
                        player.hp = 100
                    self.bullet_list.remove(bullet)

    def player_collision_processing(self, player_name):
        ejection = [0, 0]

        sides = []
        for block in self.block_list:
            side = count_sides(self.player_dict[player_name], block)
            if contact_block_player(side):
                sides.append(side)

        if sides:
            ejection = ejection_count(sides)
            self.player_dict[player_name].pos[0] += ejection[0]
            self.player_dict[player_name].pos[1] += ejection[1]
            self.player_collision_processing(player_name)

        return ejection

    def shooting_processing(self):
        for player in self.player_dict.keys():
            if self.player_dict[player].shoot:
                self.shot_bullet_creation(player)
                self.player_dict[player].shoot = False

    def event_process(self, player_status):
        diff_pos = [player_status.player_movement[0] * self.player_dict[player_status.name].speed,
                    player_status.player_movement[1] * self.player_dict[player_status.name].speed]

        player_way_vector = [player_status.mouse_pos[0] - self.player_dict[player_status.name].pos[0],
                             player_status.mouse_pos[1] - self.player_dict[player_status.name].pos[1]]

        self.move_player(player_status.name, diff_pos, player_way_vector)
        if player_status.shoot:
            self.shot_bullet_creation(player_status.name)

    def angle_of_track(self, way_vector):  # way in radians
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

    def shot_bullet_creation(self, player_name):
        way_angle = self.angle_of_track(self.player_dict[player_name].way_vector)

        bullet_pos = self.player_dict[player_name].pos

        bullet_vector = [0, 0]
        bullet_vector[0] = math.cos(way_angle)
        bullet_vector[1] = math.sin(way_angle)

        self.bullet_list.append(Bullet(self.bullet_counter,
                                       bullet_pos, 5,
                                       (200, 200, 100), 10, self.bullet_speed,
                                       bullet_vector,
                                       player_name))

    def move_player(self, player_name, diff_pos, way_vector):
        self.player_dict[player_name].pos[0] += diff_pos[0]
        self.player_dict[player_name].pos[1] += diff_pos[1]
        self.player_dict[player_name].way_vector = way_vector


def count_sides(player, block):
    """
    Count distance that the player should make on a specific side to go out of the block.
    If one of the sides is negative, the player is out of the block.
    """

    left_side = player.pos[0] + player.radius - block.x
    up_side = player.pos[1] + player.radius - block.y
    right_side = block.x + block.width - player.pos[0] + player.radius
    down_side = block.y + block.width - player.pos[1] + player.radius

    return left_side, up_side, right_side, down_side


def contact_block_player(side):
    if side[0] > 0 and side[1] > 0 and side[2] > 0 and side[3] > 0:
        return True
    return False


def ejection_count(sides):
    """
    Find the shortest side in which player should move to go out of the block and count ejection.
    """

    left_side, up_side, right_side, down_side = sides[0]
    ejection = [0, 0]

    if left_side <= up_side and left_side <= down_side:
        ejection[0] = -left_side
    elif right_side <= up_side and right_side <= down_side and not double_horizontal_contact(sides):
        ejection[0] = right_side
    elif up_side < down_side:
        ejection[1] = -up_side
    else:
        ejection[1] = down_side

    return ejection


def double_horizontal_contact(sides):
    if len(sides) >= 2:
        if abs(sides[0][0] - sides[1][2]) < abs(sides[0][1] - sides[1][3]):
            return True
    return False


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
