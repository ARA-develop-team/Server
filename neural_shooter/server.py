"""game server"""

import socket
import threading
import pickle
from multiprocessing import Process
from typing import List, Any

import config_parser as parser
import server_field
import player as pl

print('Hello from ARA-development🦜')

"""Old version"""
# def send(client, message, local=False):
#     packed_message = pickle.dumps(message)  # packing message
#
#     # send length
#     if not local:
#         message_length = len(packed_message)
#         send_length = str(message_length).encode(Server.FORMAT)
#         send_length += b' ' * (Server.HEADER - len(send_length))
#         client.send(send_length)
#
#     # send message
#     client.send(packed_message)


def send(client, message):
    packed_message = pickle.dumps(message)  # packing message

    # send length
    message_length = len(packed_message)
    send_length = str(message_length).encode(Server.FORMAT)
    send_length += b' ' * (Server.HEADER - len(send_length))
    client.send(send_length)

    # send message
    client.send(packed_message)


def receive(client):

    message_length = int(client.recv(Server.HEADER).decode(Server.FORMAT))

    # reception message
    message = client.recv(message_length)
    message = pickle.loads(message)  # unpacking message

    return message


class VisualServer:  # connection with visual server thread
    FORMAT = 'utf-8'
    visual_serv = socket.socket()

    def __init__(self, PORT):
        reconnection_num = 0
        while True:
            try:
                self.visual_serv.connect(('localhost', PORT))
                print('Connected')
                break

            except ConnectionRefusedError:
                print(f'RECONNECTION {reconnection_num}')
                reconnection_num += 1

        print('init definition ended')

    def add(self, mess_type, data):
        # to show message on screen USE self.output() instead of print()
        # mess_type = 0 - showing output of program; mess_type = 1 - showing data of players

        package = [mess_type, data]

        """
        Old version
        send(self.visual_serv, package, local=True)
        """
        packed_message = pickle.dumps(package)
        self.visual_serv.send(packed_message)


class Server:
    yml_data1 = parser.getting_socket_data(r'server.yml')
    yml_data2 = parser.getting_start_data(r'start.yml')

    VS_run = yml_data2['VS_run']      # run VisualServer or not
    HEADER = 64
    ADDR = (yml_data1['IP'], yml_data1['PORT'])
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name):
        self.name = name
        self.main_field = server_field.ServerField(Server.yml_data2['start_vector'], Server.yml_data2['screen_size'])
        self.visual_server = None

    def start_with_visual_server(self):
        """
        Visual server preparation and start running server.
        """

        import visual_server

        try:
            deployed_server, deployed_port = visual_server.server_deploy(PORT=self.yml_data1['VPORT'],
                                                                         extra_PORT=self.yml_data1['extra_VPORT'])

            visual_thread = Process(target=self.start, args=(deployed_port, ))
            visual_thread.start()
            visual_server.start(IP_PORT=Server.ADDR, SERVER=deployed_server, LOCAL_PORT=deployed_port)

        except OSError:
            raise Exception('PORTS %s and %s are busy. Server could not be deployed' %
                            (self.yml_data1['VPORT'], self.yml_data1['extra_VPORT']))

        else:
            pass

    def start(self, deployed_port=0):
        if self.VS_run:
            self.visual_server = VisualServer(deployed_port)

        thread = threading.Thread(target=self.game_mechanics)
        thread.start()

        Server.socket.bind(Server.ADDR)
        Server.socket.listen()

        self.output(f"[LISTENING] Server is listening on {Server.ADDR[0]}")

        while True:
            conn, addr = Server.socket.accept()
            self.output(f"[NEW CONNECTION] {addr} connected.")

            player_name = conn.recv(Server.HEADER).decode('utf-8')
            self.output(f"PLAYER NAME - {player_name}")

            if self.VS_run:
                self.visual_server.add(1, player_name)

            new_player = pl.Player(Server.yml_data2['start_point'], Server.yml_data2['user_color'],
                                   Server.yml_data2['color_lines'], Server.yml_data2['user_speed'],
                                   Server.yml_data2['color_info'],
                                   Server.yml_data2['user_radius'][0], Server.yml_data2['user_radius'][1], player_name)

            self.main_field.player_dict[player_name] = new_player

            self.output(f"[ACTIVE CONNECTIONS] {threading.active_count()}")  # Anton change activeCount --> active_count
            thread = threading.Thread(target=self.handle_client, args=(conn, addr, player_name))
            thread.start()

    def handle_client(self, conn, addr, name):  # working with client

        connected = True
        while connected:

            send(conn, [self.main_field.player_dict, self.main_field.block_list, self.main_field.bullet_list])

            message = receive(conn)
            if message == "PLAYER DISCONNECT":
                self.output(f'[DISCONNECT] player {name} disconnect')
                connected = False
                self.main_field.player_dict.pop(name)
            elif type(message) == "string":
                print(f'[WARNING] Client: {name} Addr: {addr} send message type string')
            else:
                self.main_field.event_process(message)

        conn.close()

    def game_mechanics(self):
        while True:
            self.main_field.bullets_processing()

    def output(self, string):
        if self.VS_run:
            self.visual_server.add(0, string)
        else:
            print(string)


if __name__ == '__main__':
    main_server = Server(__name__)
    if main_server.VS_run:
        main_server.start_with_visual_server()
    else:
        main_server.start()
