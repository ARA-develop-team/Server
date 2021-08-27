"""game server"""

import socket
import threading
import pickle
from multiprocessing import Process

import config_parser as parser
import server_field
import player as pl
import visual_server

print('Hello from ARA-development🦜')


def send(client, message):
    print(f'send: {message}')
    # send length
    packed_message = pickle.dumps(message)  # packing message
    message_length = len(packed_message)
    send_length = str(message_length).encode(Server.FORMAT)
    send_length += b' ' * (Server.HEADER - len(send_length))
    client.send(send_length)

    # send message
    client.send(packed_message)


def receive(client):
    message_length = client.recv(Server.HEADER).decode(Server.FORMAT)
    # reception message
    if type(message_length) == 'int':
        message = client.recv(message_length)
        message = pickle.loads(message)  # unpacking message
    else:
        message = message_length
    print(f'receive: {message}')
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

    def show(self, data):
        pass
        # self.visual_serv.sendall(bytes(data))


class Server:
    yml_data1 = parser.getting_socket_data(r'server.yml')
    yml_data2 = parser.getting_start_data(r'start.yml')

    VS_run = True      # run VisualServer or not
    HEADER = 64
    ADDR = (yml_data1['IP'], yml_data1['PORT'])
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name):
        self.name = name
        self.main_field = server_field.ServerField(Server.yml_data2['screen_size'], Server.yml_data2['user_radius'][0])
        self.screen = None

    def preparation(self):
        if self.VS_run:
            import visual_server

            try:
                deployed_server, deployed_port = visual_server.server_deploy(PORT=self.yml_data1['VPORT'],
                                                                             extra_PORT=self.yml_data1['extra_VPORT'])

                visual_thread = Process(target=self.start, args=(deployed_port, ))
                visual_thread.start()

                visual_server.start(Server.ADDR, deployed_server, deployed_port)

            except OSError:
                raise Exception('PORTS %s and %s are busy. Server could not be deployed' %
                                (self.yml_data1['VPORT'], self.yml_data1['extra_VPORT']))

            else:
                pass

        else:
            self.start()

    def start(self, deployed_port=0):
        if self.VS_run:
            self.screen = VisualServer(deployed_port)

        thread = threading.Thread(target=self.game_mechanics)
        thread.start()

        Server.socket.bind(Server.ADDR)
        Server.socket.listen()

        if self.VS_run:
            print(f"[LISTENING] Server is listening on {Server.ADDR[0]}")
            self.screen.show(f"\n[LISTENING] Server is listening on {Server.ADDR[0]}")
        else:
            print(f"[LISTENING] Server is listening on {Server.ADDR[0]}")

        while True:
            conn, addr = Server.socket.accept()
            print(f"[NEW CONNECTION] {addr} connected.")

            player_name = conn.recv(Server.HEADER).decode('utf-8')
            print(f"PLAYER NAME - {player_name}")
            # self.main_field.player_dict[player_name] = None

            new_player = pl.Player(Server.yml_data2['start_point'], Server.yml_data2['user_color'],
                                   Server.yml_data2['color_lines'], Server.yml_data2['user_speed'],
                                   Server.yml_data2['color_info'],
                                   Server.yml_data2['user_radius'][0], Server.yml_data2['user_radius'][1], player_name)
            self.main_field.player_dict[player_name] = new_player

            block_package_list = []
            for block in self.main_field.block_list:
                block_package_list.append(block.get_data_package(3))

            send(conn, [new_player.get_data_package(3), block_package_list])

            print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")  # Anton change activeCount --> active_count
            thread = threading.Thread(target=self.handle_client, args=(conn, addr, player_name))
            thread.start()

    def handle_client(self, conn, addr, name):  # working with client
        player_list = [name]
        connected = True
        while connected:

            message = receive(conn)
            if message == "PLAYER DISCONNECT":
                connected = False
                self.main_field.player_dict.pop(name)
                print(f'[DISCONNECT] player {name} disconnect')
            elif type(message) == "string":
                print(f'[WARNING] Client: {name} Addr: {addr} send message type string')
            else:

                if name in self.main_field.player_dict.keys():
                    self.main_field.player_dict[name].update_data(message)
                else:
                    player_list.remove(name)
                    print(f'player {name} dead')

                if message[1]:
                    self.main_field.bullet_list.append(pl.CBullet(self.main_field.player_dict[name].pos, 5,
                                                                  (200, 200, 100), 10, 3,
                                                                  self.main_field.player_dict[name].way_vector,
                                                                  name))

                player_package_list, block_package_list, bullet_package_list = [], [], []

                for player in self.main_field.player_dict.values():
                    if player.name not in player_list:
                        player_list.append(player.name)
                        player_package_list.append(player.get_data_package(3))
                    else:
                        player_package_list.append(player.get_data_package(2))

                for block in self.main_field.block_list:
                    block_package_list.append(block.get_data_package(1))

                for bullet in self.main_field.bullet_list:
                    bullet_package_list.append(bullet.get_data_package())

                if len(block_package_list) == 0:
                    block_package_list = None

                send(conn, [player_package_list, block_package_list, bullet_package_list])

        conn.close()

    def game_mechanics(self):
        while True:
            self.main_field.main()


if __name__ == '__main__':
    main_server = Server(__name__)
    main_server.preparation()

# file_path = 'server.yml'
# yml_data = parser.getting_socket_data(file_path)
#
# HEADER = 64
# ADDR = (yml_data['IP'], yml_data['PORT'])
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)
#
# pos_player = {}
#
#
# def handle_client(conn, addr, number):
#     print(f"[NEW CONNECTION] {addr} connected.")
#     connected = True
#     while connected:
#         # reception length
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length == "PLAYER DISCONNECT":
#             connected = False
#             pos_player.pop(number)
#             print(f'player #{number} disconnect')
#         elif msg_length == "NEW PLAYER":
#             pass
#         else:
#             msg_length = int(msg_length)
#             # reception message
#             msg = conn.recv(msg_length)
#
#             # treatment massage
#             msg = pickle.loads(msg)  # unpacking message
#             pos_player[number] = msg
#
#             # send length
#             msg = pickle.dumps(pos_player)  # packing message
#             msg_length = len(msg)
#             send_length = str(msg_length).encode(FORMAT)
#             send_length += b' ' * (HEADER - len(send_length))
#             conn.send(send_length)
#             # send message
#             conn.send(msg)
#
#     conn.close()
#
#
# def start():
#     server.listen()
#     index_player = 0
#     print(f"[LISTENING] Server is listening on {yml_data['IP']}")
#     while True:
#         conn, addr = server.accept()
#         print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
#         new_player = player.Player([200, 200], (25, 25, 25))
#         index_player += 1
#         pos_player[index_player] = new_player
#
#         # send length
#         msg = pickle.dumps(new_player)  # packing message
#         msg_length = len(msg)
#         send_length = str(msg_length).encode(FORMAT)
#         send_length += b' ' * (HEADER - len(send_length))
#         conn.send(send_length)
#
#         # send message
#         conn.send(msg)
#
#         thread = threading.Thread(target=handle_client, args=(conn, addr, index_player))
#         thread.start()
#
#
# print("[STARTING] server is starting...")
# start()

#     os.system("python3 server.py")
#     quit()
