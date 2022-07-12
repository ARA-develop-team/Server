import unittest
from ui.server_ui import battery_status


class Battery:
    def __init__(self):
        self.percent = None
        self.power_plugged = False


class ServerTestCase(unittest.TestCase):

    def test_battery_status(self):
        battery = Battery()

        battery.percent = 5
        self.assertEqual(battery_status(battery=battery), (0, battery.percent, battery.power_plugged))

        battery.percent = 10
        self.assertEqual(battery_status(battery=battery), (1, battery.percent, battery.power_plugged))

        battery.percent = 30
        self.assertEqual(battery_status(battery=battery), (2, battery.percent, battery.power_plugged))

        battery.percent = 50
        self.assertEqual(battery_status(battery=battery), (3, battery.percent, battery.power_plugged))

        battery.percent = 70
        self.assertEqual(battery_status(battery=battery), (4, battery.percent, battery.power_plugged))

        battery.percent = 90
        self.assertEqual(battery_status(battery=battery), (5, battery.percent, battery.power_plugged))

        battery.percent = 110
        self.assertEqual(battery_status(battery=battery), (6, battery.percent, battery.power_plugged))

        battery.percent = 0
        self.assertEqual(battery_status(battery=battery), (6, battery.percent, battery.power_plugged))


if __name__ == '__main__':
    unittest.main()
