"""game client (player)"""
import pickle
import socket
import config_parser as parser

file_path = r'client.yml'
yml_data = parser.getting_data(file_path)

# PORT = 1111
# SERVER = " "

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ["!DISCONNECT", "!DISCONNECT_FROM_SERVER"]
ADDR = (yml_data['IP'], yml_data['PORT'])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def data_exchange(msg):
    # send length
    message = pickle.dumps(msg)  # packing message
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    # send message
    client.send(message)

    # reception length
    ans_length = client.recv(HEADER).decode(FORMAT)
    ans_length = int(ans_length)

    # reception message
    ans = client.recv(ans_length)
    return pickle.loads(ans)


def connect():
    client.send(b'CONNECT')

    # reception length
    ans_length = client.recv(HEADER).decode(FORMAT)
    ans_length = int(ans_length)

    # reception message
    ans = client.recv(ans_length)
    return pickle.loads(ans)

