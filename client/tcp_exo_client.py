import socket

IP = '176.38.153.161'
port = 8585

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, port))

result = sock.recv(1024)
print(result)

number = 0
run = True
while run:
    number += 1
    mess = bytes(str(number), 'utf-8')
    sock.send(mess)
sock.close()
