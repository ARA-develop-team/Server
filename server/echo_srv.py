import socket
server = True
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('192.168.10.191', 8585))
while server:
    result = sock.recv(1024)
    print('Сonnection', result.decode('utf-8'))
    print(str(result))
    if str(result) == "b'quit'":
        server = False
sock.close()
