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

    def signing_off(self):  # FIN massage
        self.send(Client.DISCONNECT_MESSAGE)
        self.socket.close()

    def send(self, message):
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
        return message
