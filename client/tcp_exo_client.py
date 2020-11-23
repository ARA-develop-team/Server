import socket

IP = '176'
port = 8585

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, port))
run = True
while run:
    result = sock.recv(1024)
    print(result)
    mess = input('')
    mess = bytes(mess, 'utf-8')
    sock.send(mess)
sock.close()
