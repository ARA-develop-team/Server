"""game client (player)"""

import pickle
import socket
import config_parser as parser


class Client:
    yml_data = parser.getting_socket_data(r'client.yml')
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = ["!DISCONNECT", "!DISCONNECT_FROM_SERVER"]

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name):
        self.name = name
        self.SERVER_ADDR = 'None'

    def connect(self, addr=(yml_data['IP'], yml_data['PORT'])):
        self.SERVER_ADDR = addr
        Client.socket.connect(addr)
        name = self.name.encode(Client.FORMAT)
        Client.socket.send(name)

        # reception length
        ans_length = Client.socket.recv(Client.HEADER).decode(Client.FORMAT)
        ans_length = int(ans_length)

        # reception message
        ans = Client.socket.recv(ans_length)
        ans = pickle.loads(ans)
        return ans

    def data_exchange(self, msg):
        # send length
        message = pickle.dumps(msg)  # packing message
        msg_length = len(message)
        send_length = str(msg_length).encode(Client.FORMAT)
        send_length += b' ' * (Client.HEADER - len(send_length))
        Client.socket.send(send_length)

        # send message
        Client.socket.send(message)

        # reception length
        ans_length = Client.socket.recv(Client.HEADER).decode(Client.FORMAT)
        ans_length = int(ans_length)

        # reception message
        ans = Client.socket.recv(ans_length)
        ans = pickle.loads(ans)
        return ans

    def signing_off(self):  # FIN massage
        Client.socket.send(b'PLAYER DISCONNECT')
        Client.socket.close()

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
