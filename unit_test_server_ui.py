import unittest
# from ui.server_ui import battery_status
import src


def map_creation(map, block_size):
    obj_list = []

    obj_width = block_size[0]
    obj_height = block_size[1]

    obj_y = 0
    for block in range(len(map)):
        obj_x = 0
        for kind in map[block]:
            if kind == 1:
                obj_list.append(src.field.Block(block, obj_x, obj_y, obj_width, obj_height, kind))

            obj_x += obj_width
        obj_y += obj_height

    return obj_list


class CollisionTestCase(unittest.TestCase):
    
    def test_collision(self):
        radius = 5
        mid_pos = [15, 15]
        map = [[1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]]
        
        field = src.ServerField((0, 0), (500, 500))
        field.block_list = map_creation(map, (10, 10))

        for x in range(7, 23):
            for y in range(7, 23):
                
                player = src.Player([x, y], (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), radius, 20, "test")
                
                field.player_dict["test"] = player
                field.player_collision_processing("test")
                print(field.player_dict["test"].pos)
                print(mid_pos)
                self.assertEqual(field.player_dict["test"].pos, mid_pos)
                  
class OneBlockCollision(unittest.TestCase):
    PLAYER_RADIUS = 5
    BLOCK_SIZE = 10

    map = [[0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]]
    
    field = src.ServerField((0, 0), (500, 500))
    field.block_list = map_creation(map, (BLOCK_SIZE, BLOCK_SIZE))

    def test_player_collision_processing(self):
        # TEST_CASES = [[[10, 12], [5, 12]], [[10, 14], [5, 14]], [[13, 11], [13, 5]], [[17, 11], [17, 5]], [[19, 11], [25, 11]], [[19, 11], [25, 11]]]
        y = 12
        for x in range(13, 17):
            player_pos = [x, y]
            target_pos = [x, 5]
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            self.field.player_dict["test"] = player
            self.field.player_collision_processing("test")
            self.assertEqual(self.field.player_dict["test"].pos, target_pos)

        x = 18
        for y in range(13, 17):
            player_pos = [x, y]
            target_pos = [25, y]
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            self.field.player_dict["test"] = player
            self.field.player_collision_processing("test")
            self.assertEqual(self.field.player_dict["test"].pos, target_pos)

        y = 18
        for x in range(13, 17):
            player_pos = [x, y]
            target_pos = [x, 25]
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            self.field.player_dict["test"] = player
            self.field.player_collision_processing("test")
            self.assertEqual(self.field.player_dict["test"].pos, target_pos)

        x = 12
        for y in range(13, 17):
            player_pos = [x, y]
            target_pos = [5, y]
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            self.field.player_dict["test"] = player
            self.field.player_collision_processing("test")
            self.assertEqual(self.field.player_dict["test"].pos, target_pos)
                
    def test_count_sides_ejection_count(self):
        TEST_CASES = [[[10, 12], [-5, 0]], [[10, 14], [-5, 0]], [[13, 11], [0, -6]], [[17, 11], [0, -6]], [[19, 11], [6, 0]], [[19, 11], [6, 0]]]
        block = self.field.block_list[0]
        for player_pos, target_pos in TEST_CASES:
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            result = src.ejection_count([src.count_sides(player, block)])
            self.assertEqual(result, target_pos)

class ThreeBlackCollision(unittest.TestCase):
    PLAYER_RADIUS = 5
    BLOCK_SIZE = 10

    map = [[0, 1, 0],
           [1, 1, 1],
           [0, 1, 0]]
    
    field = src.ServerField((0, 0), (500, 500))
    field.block_list = map_creation(map, (BLOCK_SIZE, BLOCK_SIZE))

    def test_player_collision_processing(self):
        TEST_CASES = [[[11, 11], [5, 5]], [[19, 11], [25, 5]], [[19, 19], [25, 25]], [[11, 19], [5, 25]]]
        for player_pos, target_pos in TEST_CASES:
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            self.field.player_dict["test"] = player
            self.field.player_collision_processing("test")
            self.assertEqual(self.field.player_dict["test"].pos, target_pos)

    def test_count_sides_ejection_count(self):
        TEST_CASES = [[[11, 11], [-6, -6]], [[19, 11], [6, -6]], [[19, 19], [6, 6]], [[11, 19], [-6, 6]]]
        blocks = self.field.block_list
        for player_pos, target_pos in TEST_CASES:
            player = src.Player(player_pos, (0, 0, 0), (0, 0, 0), 1, (0, 0, 0), self.PLAYER_RADIUS, 20, "test")
            sides = []
            for block in blocks:
                side = src.count_sides(player, block)
                sides.append(side)
                
            result = src.ejection_count(sides)
            self.assertEqual(result, target_pos)



class Battery:
    def __init__(self):
        self.percent = None
        self.power_plugged = False


# class ServerTestCase(unittest.TestCase):

#     def test_battery_status(self):
#         battery = Battery()

#         battery.percent = 5
#         self.assertEqual(battery_status(battery=battery), (0, battery.percent, battery.power_plugged))

#         battery.percent = 10
#         self.assertEqual(battery_status(battery=battery), (1, battery.percent, battery.power_plugged))

#         battery.percent = 30
#         self.assertEqual(battery_status(battery=battery), (2, battery.percent, battery.power_plugged))

#         battery.percent = 50
#         self.assertEqual(battery_status(battery=battery), (3, battery.percent, battery.power_plugged))

#         battery.percent = 70
#         self.assertEqual(battery_status(battery=battery), (4, battery.percent, battery.power_plugged))

#         battery.percent = 90
#         self.assertEqual(battery_status(battery=battery), (5, battery.percent, battery.power_plugged))

#         battery.percent = 110
#         self.assertEqual(battery_status(battery=battery), (6, battery.percent, battery.power_plugged))

#         battery.percent = 0
#         self.assertEqual(battery_status(battery=battery), (6, battery.percent, battery.power_plugged))


if __name__ == '__main__':
    unittest.main()
