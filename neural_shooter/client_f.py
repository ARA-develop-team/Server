"""game client (player)"""
import pickle
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ["!DISCONNECT", "!DISCONNECT_FROM_SERVER"]
SERVER = "192.168.0.145"
ADDR = (SERVER, PORT)

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
