import socket
server = True
IP = input()
port = int(input())
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, port))
while server:
    result = sock.recv(1024)
    print('Сonnection', result.decode('utf-8'))
    print(str(result))
    if str(result) == "b'quit'":
        server = False
sock.close()
