"""game client (player)"""

import pickle
import socket
import config_parser as parser


class Client:
    yml_data = parser.getting_socket_data(r'client.yml')
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = 'PLAYER DISCONNECT'

    def __init__(self, name):
        self.name = name
        self.SERVER_ADDR = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, addr=(yml_data['IP'], yml_data['PORT'])):
        print(addr)
        self.SERVER_ADDR = addr
        self.socket.connect(addr)
        name = self.name.encode(Client.FORMAT)
        self.socket.send(name)

    def data_exchange(self, msg):
        player_package_list, block_package_list, bullet_package_list = self.receive()

        self.send(msg)

        return player_package_list, block_package_list, bullet_package_list

    def signing_off(self):  # FIN massage
        self.send(Client.DISCONNECT_MESSAGE)
        self.socket.close()

    def send(self, message):
        # print(f'send: {message}')
        # send length
        packed_message = pickle.dumps(message)  # packing message
        message_length = len(packed_message)
        send_length = str(message_length).encode(Client.FORMAT)
        send_length += b' ' * (Client.HEADER - len(send_length))
        self.socket.send(send_length)

        # send message
        self.socket.send(packed_message)

    def receive(self):
        message_length = int(self.socket.recv(Client.HEADER).decode(Client.FORMAT))

        # reception message
        message = self.socket.recv(message_length)
        message = pickle.loads(message)  # unpacking message
        # print(f'receive: {message}')
        return message


# file_path = r'client.yml'
# yml_data = parser.getting_socket_data(file_path)
#
# HEADER = 64
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = ["!DISCONNECT", "!DISCONNECT_FROM_SERVER"]
# ADDR = (yml_data['IP'], yml_data['PORT'])
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)
#
#
# def data_exchange(msg):
#     # send length
#     message = pickle.dumps(msg)  # packing message
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#
#     # send message
#     client.send(message)
#
#     # reception length
#     ans_length = client.recv(HEADER).decode(FORMAT)
#     ans_length = int(ans_length)
#
#     # reception message
#     ans = client.recv(ans_length)
#     ans = pickle.loads(ans)
#     return ans
#
#
# def connect():
#     client.send(b'NEW PLAYER')
#
#     # reception length
#     ans_length = client.recv(HEADER).decode(FORMAT)
#     ans_length = int(ans_length)
#
#     # reception message
#     ans = client.recv(ans_length)
#     return pickle.loads(ans)
#
#
# def signing_off():  # FIN massage
#     client.send(b'PLAYER DISCONNECT')
#     client.shutdown(socket.SHUT_RDWR)
#     client.close()
