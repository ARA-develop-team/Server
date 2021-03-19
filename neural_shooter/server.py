"""game server"""

import socket
import threading
import pickle
import config_parser as parser


class Server():
    yml_data = parser.getting_socket_data(r'server.yml')
    HEADER = 64
    ADDR = (yml_data['IP'], yml_data['PORT'])
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name):
        self.name = name
        self.players = {}

    def start(self):
        Server.server_socket.bind(Server.ADDR)
        Server.server_socket.listen()
        print(f"[LISTENING] Server is listening on {Server.ADDR[0]}")
        while True:
            conn, addr = Server.server_socket.accept()
            print(f"[NEW CONNECTION] {addr} connected.")

            player_name = conn.recv(Server.HEADER).decode('utf-8')
            print(f"PLAYER NAME - {player_name}")
            self.players[player_name] = 'None'

            # send length
            msg = pickle.dumps(self.players)  # packing message
            msg_length = len(msg)
            send_length = str(msg_length).encode(Server.FORMAT)
            send_length += b' ' * (Server.HEADER - len(send_length))
            conn.send(send_length)

            # send message
            conn.send(msg)

            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()}")
            thread = threading.Thread(target=self.handle_client, args=(conn, addr, player_name))
            thread.start()

    def handle_client(self, conn, addr, name):
        connected = True
        while connected:
            # reception length
            msg_length = conn.recv(Server.HEADER).decode(Server.FORMAT)

            if msg_length == "PLAYER DISCONNECT":
                connected = False
                self.players.pop(name)
                print(f'[DISCONNECT] player {name} disconnect')
            elif type(msg_length) == "string":
                print(f'[WARNING] Client: {name} Addr: {addr} send message type string')

            else:
                msg_length = int(msg_length)
                # reception message
                msg = conn.recv(msg_length)
                msg = pickle.loads(msg)  # unpacking message

                # treatment massage
                self.players[name] = msg

                # send length
                msg = pickle.dumps(self.players)  # packing message
                msg_length = len(msg)
                send_length = str(msg_length).encode(Server.FORMAT)
                send_length += b' ' * (Server.HEADER - len(send_length))
                conn.send(send_length)
                # send message
                conn.send(msg)

        conn.close()


main_server = Server('main')
main_server.start()

# file_path = r'server.yml'
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
