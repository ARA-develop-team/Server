import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mess = input('')
mess = bytes(mess, 'utf-8')
sock.sendto(mess, ('176.38.153.161', 8585))
