"""graphical interface for server"""

import socket
import threading
import speedtest
import psutil
from sys import platform

from kivy.clock import mainthread
from kivy.uix.widget import Widget
from kivy.uix.treeview import TreeViewLabel
from kivy.app import App
from kivy.config import Config


def get_screen_dimensions_linux():
    xrandrOutput = str(subprocess.Popen(['xrandr'], stdout=subprocess.PIPE).communicate()[0])
    matchObj = re.findall(r'current\s(\d+) x (\d+)', xrandrOutput)
    if matchObj:
        return [int(matchObj[0][0]), int(matchObj[0][1])]


if platform == "linux" or platform == "linux2":
    import subprocess
    import re
    screen_dimensions = get_screen_dimensions_linux()

elif platform == "win32":
    from win32api import GetSystemMetrics
    screen_dimensions = [GetSystemMetrics(0), GetSystemMetrics(1)]

else:
    raise Exception(f"Platform {platform} can't be used")

FULL_HD = 0  # 1 = True, 0 = False (HD)
size = [(1280, 720), screen_dimensions]

Config.set('graphics', 'width', size[FULL_HD][0])
Config.set('graphics', 'height', size[FULL_HD][1])

try: 
    test = speedtest.Speedtest()
except speedtest.SpeedtestBestServerFailure:
    print("Speedtest do not working!!!")


class GraphicLayout(Widget):
    is_run = True
    tree_view_label_list = [TreeViewLabel(text='percent: ___'), TreeViewLabel(text='power plugged: ___'),
                            TreeViewLabel(text='download speed: ___'), TreeViewLabel(text='upload speed: ___'),
                            TreeViewLabel(text='ping: ___')]

    def __init__(self, server_data, server, **kwargs):
        super(GraphicLayout, self).__init__(**kwargs)

        self.server_data = server_data
        self.link = 'https://github.com/ARA-develop-team'
        self.FULL_HD = FULL_HD

        # connection with main server
        self.server = server
        self.preparing()

        # thread for updating local data
        self.update_local_data = threading.Thread(target=self.local_update)
        self.update_local_data.setDaemon(True)
        ServerApp.threads.append(self.update_local_data)  # for join it in the end
        self.update_local_data.start()

    def preparing(self):
        try:
            conn, address = self.server.accept()
            self.ids.console.text += f'>>> [VISUAL] connected: {address}'

        except AttributeError:
            self.ids.console.text += f"\n>>> [AttributeError] '{self.server}' has no attribute 'accept'"
        # print('[VISUAL] connected:', address)

    def tree_view(self):
        # tree view creation
        item1 = self.ids.treeview.add_node(TreeViewLabel(text='SERVER'))
        self.ids.treeview.add_node(TreeViewLabel(text=f'HOST: {self.server_data[0][0]}'), item1)
        self.ids.treeview.add_node(TreeViewLabel(text=f'PORT: {self.server_data[0][1]}'), item1)
        self.ids.treeview.add_node(TreeViewLabel(text=f'LOCAL PORT: {self.server_data[1]}'), item1)

        item2 = self.ids.treeview.add_node(TreeViewLabel(text='BATTERY'))
        self.ids.treeview.add_node(self.tree_view_label_list[0], item2)
        self.ids.treeview.add_node(self.tree_view_label_list[1], item2)

        item3 = self.ids.treeview.add_node(TreeViewLabel(text='SPEED TEST'))
        self.ids.treeview.add_node(self.tree_view_label_list[2], item3)
        self.ids.treeview.add_node(self.tree_view_label_list[3], item3)
        self.ids.treeview.add_node(self.tree_view_label_list[4], item3)

        item4 = self.ids.treeview.add_node(TreeViewLabel(text='PLAYERS'))

    def local_update(self):
        self.tree_view()
        last_battery_info = [None, None, None]  # start info about battery, updating after every changing
        while self.is_run:
            # battery data update
            status, percent, is_power_plugged = battery_status(battery=psutil.sensors_battery())
            power_plugged = 'on' if is_power_plugged is True else 'off'

            if status != last_battery_info[0]:  # update icon if it's necessary
                self.screen_update(status)
                last_battery_info[0] = status

            # update text in TreeView if it's necessary
            if percent != last_battery_info[1] or power_plugged != last_battery_info[2]:
                self.tree_view_label_list[0].text = f'percent: {int(percent)}%'
                self.tree_view_label_list[1].text = f'power plugged: {power_plugged}'
                last_battery_info[1], last_battery_info[2] = percent, power_plugged

            # speed test data update in TreeView
            if self.is_run is True:     # for faster closing program
                download = speed_test('download')
                self.tree_view_label_list[2].text = f'download speed: {int((download / 1024) / 1024)} Mb/s'

            if self.is_run is True:     # for faster closing program
                upload, ping = speed_test('upload+ping')
                self.tree_view_label_list[3].text = f'upload speed : {int((upload / 1024) / 1024)} Mb/s'
                self.tree_view_label_list[4].text = f'ping : {int(ping)} ms'

    @mainthread
    def screen_update(self, status):  # for img
        self.ids.battery_indicator.icon = f'sprites/icon_battery{status}.png'

    def input_processing(self):  # data from console
        commands_list = ['clear', 'info', '@']
        # get text to console (processing some commands) and clear input line
        if self.ids.input.text == commands_list[0]:  # clear console
            self.ids.console.text = ""
        elif self.ids.input.text == 'info':
            self.ids.console.text += '\n>>> commands: {} - for clear console\n                 ' \
                                     '                {} - for look available commands\n                 ' \
                                     '                {}your text - for get text text to console without warnings' \
                                     ''.format(*commands_list)

        elif len(self.ids.input.text) != 0 and self.ids.input.text[0] == '@':
            self.ids.console.text += f'\n>>> {self.ids.input.text[1:]}'

        elif len(self.ids.input.text) == 0:
            self.ids.console.text += f'\n>>>'

        else:
            self.ids.console.text += f'\n>>> {self.ids.input.text}  -- command not found, try info'

        self.ids.input.text = ""

    def change_screen_size(self):           # rewrite in the future
        if self.FULL_HD == 0:
            self.FULL_HD = 1
        else:
            self.FULL_HD = 0
        # Window.fullscreen = True
        # Window.size = (size[self.FULL_HD][0], size[self.FULL_HD][1])

    def git_link(self):
        import webbrowser
        webbrowser.open(self.link)  # Go to our git


class ServerApp(App):
    threads = []

    def __init__(self, ip, port, server, local_port):
        super(ServerApp, self).__init__()
        self.server = server
        self.local_port = local_port
        self.info_main_server = [ip, port]

    def build(self):
        update_data = threading.Thread(target=self.update)  # thread for updating data from main server code
        update_data.start()

        return GraphicLayout([self.info_main_server, self.local_port], self.server)

    def on_stop(self):
        GraphicLayout.is_run = False
        for thread in self.threads:     # closing all threads
            thread.join()

    def update(self):
        pass
        # conn, address = self.server.accept()
        # print('[VISUAL] connected:', address)
        # server_data = conn.recv(1024)
        # server_data = list(server_data)
        # print('[VISUAL] ', server_data)

        # server_data = conn.recv(1024)
        # server_data = list(server_data)
        # print('[VISUAL] ', server_data)


'''external functions'''


def start(server_data, server, local_port):
    # visual = ServerApp(*server_data, server)
    # visual.run()
    ServerApp(*server_data, server, local_port).run()


def server_deploy(HOST='', PORT=9090, extra_PORT=8080):
    sock = socket.socket()
    try:
        sock.bind((HOST, PORT))
        sock.listen(1)
        final_port = PORT

    except OSError:  # in case first port is already opened
        sock.bind((HOST, extra_PORT))
        sock.listen(1)
        final_port = extra_PORT

    return sock, final_port


def battery_status(battery=psutil.sensors_battery()):
    if 0 < int(battery.percent) < 10:
        status = 0
    elif 10 <= int(battery.percent) < 30:
        status = 1
    elif 30 <= int(battery.percent) < 50:
        status = 2
    elif 50 <= int(battery.percent) < 70:
        status = 3
    elif 70 <= int(battery.percent) < 90:
        status = 4
    elif 90 <= int(battery.percent) <= 100:
        status = 5
    else:
        status = 6
    return status, battery.percent, battery.power_plugged


def speed_test(case):
    if case == 'download':
        download = test.download()
        return download

    elif case == 'upload+ping':
        upload = test.upload()
        ping = test.results.ping
        return upload, ping

    else:
        print(f"Unknown case: {case}")


if __name__ == '__main__':
    ServerApp('[server ip]', '[server port]', 'serv', '[local port]').run()

    # conn, address = sock.accept()
    # print('[VISUAL] connected:', address)
    # server_data = conn.recv(1024)
    # server_data = list(server_data)
    # print('[VISUAL] ', server_data)
