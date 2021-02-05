"""game server"""
import socket
import threading
import pickle

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

pos_player = []


def handle_client(conn, addr, number):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # reception length
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        # reception message
        msg = conn.recv(msg_length)

        # treatment massage
        msg = pickle.loads(msg) # unpacking message
        pos_player[number] = msg

        # send length
        msg = pickle.dumps(pos_player)  # packing message
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        # send message
        conn.send(msg)

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        pos_player.append([])
        thread = threading.Thread(target=handle_client, args=(conn, addr, threading.activeCount() - 1))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
