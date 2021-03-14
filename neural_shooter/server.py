"""game server"""

import socket
import threading
import pickle
import config_parser as parser
import player

file_path = r'server.yml'
yml_data = parser.getting_socket_data(file_path)

HEADER = 64
ADDR = (yml_data['IP'], yml_data['PORT'])
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

pos_player = {}


def handle_client(conn, addr, number):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # reception length
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length == "PLAYER DISCONNECT":
            connected = False
            pos_player.pop(number)
            print(f'player #{number} disconnect')
        elif msg_length == "NEW PLAYER":
            pass
        else:
            msg_length = int(msg_length)
            # reception message
            msg = conn.recv(msg_length)

            # treatment massage
            msg = pickle.loads(msg)  # unpacking message
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
    index_player = 0
    print(f"[LISTENING] Server is listening on {yml_data['IP']}")
    while True:
        conn, addr = server.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        # new_player = player.Player([200, 200], (25, 25, 25))
        new_player = 1
        index_player += 1
        pos_player[index_player] = new_player

        # send length
        msg = pickle.dumps(new_player)  # packing message
        msg_length = len(msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)

        # send message
        conn.send(msg)

        thread = threading.Thread(target=handle_client, args=(conn, addr, index_player))
        thread.start()


print("[STARTING] server is starting...")
start()
