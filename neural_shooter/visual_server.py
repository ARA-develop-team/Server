"""graphical interface for server"""

import socket
import threading
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config


def start(server_data, server):
    visual = MyApp(*server_data, server)
    update_data = threading.Thread(target=visual.update)      # thread for updating data from main server code
    update_data.start()
    visual.run()


def server_deploy(HOST='', PORT=9090, extra_PORT=8080):
    sock = socket.socket()
    try:
        sock.bind((HOST, PORT))
        sock.listen(1)
        print(f'STILL {PORT}')

    except OSError:         # in case first port is already opened
        sock.bind((HOST, extra_PORT))
        sock.listen(1)
        print(f"VISUAL SERVER in {extra_PORT}")

    return sock

    # conn, address = sock.accept()
    # print('[VISUAL] connected:', address)
    # server_data = conn.recv(1024)
    # server_data = list(server_data)
    # print('[VISUAL] ', server_data)

    # Config.set('graphics', 'resizable', 0)
    # Config.set('graphics', 'width', 700)
    # Config.set('graphics', 'height', 600)


class MyApp(App):
    def __init__(self, ip, port, server):
        super(MyApp, self).__init__()
        self.server = server
        self.label = Label(text=f'SERVER:  {ip}\nPORT:  {port}',
                           text_size=(500, 500),
                           halign='left',
                           valign='top')

    def build(self):
        box = BoxLayout(orientation='horizontal')
        box.add_widget(self.label)

        return box

    def update(self):
        conn, address = self.server.accept()
        print('[VISUAL] connected:', address)
        # server_data = conn.recv(1024)
        # server_data = list(server_data)
        # print('[VISUAL] ', server_data)


if __name__ == '__main__':
    # MyApp('ip', []).run()
    pass
