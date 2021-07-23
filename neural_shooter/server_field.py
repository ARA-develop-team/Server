
import field
import math


class ServerField:

    def __init__(self, screen_size, radius):

        self.block_list, self.width, self.height = field.map_creation(screen_size)
        self.radius = radius  # radius of player
        self.player_dict = {}
        self.bullet_list = []

    def main(self):
        for block in self.block_list:
            for player in self.player_dict.values():
                self.contact_block_player(player, block)
                for bullet in self.bullet_list:
                    print(bullet)
                    bullet.motion()
                    self.contact_bullet_player(bullet, player)
                    self.contact_bullet_block(bullet, block)

    def contact_block_player(self, player, block):
        right_side = player.pos[0] + self.radius - block.x
        up_side = player.pos[1] + self.radius - block.y
        left_side = block.x + block.width - player.pos[0] - self.radius
        down_side = block.y + block.width - player.pos[1] - self.radius

        if right_side > 0 and up_side > 0 and left_side > 0 and down_side > 0:  # if contact

            if right_side <= up_side or right_side <= down_side:
                player.pos[0] -= right_side
            if left_side <= up_side or left_side <= down_side:
                player.pos[0] -= left_side
            if up_side < down_side:
                player.pos[1] += up_side
            else:
                player.pos[1] += down_side

    def contact_bullet_player(self, bullet, player):
        if bullet.owner != player.name:
            if distance_between_two_point(player.pos, [bullet.x, bullet.y]) < self.radius + bullet.radius:
                player.hp -= bullet.damage
                self.bullet_list.remove(bullet)

    def contact_bullet_block(self, bullet, block):
        if (block.x - bullet.radius <= bullet.pos[0] <= block.x + block.width + bullet.radius) and \
                (block.y - bullet.radius <= bullet.pos[1] <= block.y + block.height + bullet.radius):
            self.bullet_list.remove(bullet)

            if block.kind == 3:
                block.health -= bullet.damage
                if block.health <= 0:
                    self.block_list.remove(block)


def distance_between_two_point(a, b):
    distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return distance
