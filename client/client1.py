import socket
IP = input()
port = int(input())
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mess = input('')
mess = bytes(mess, 'utf-8')
sock.sendto(mess, (IP, port))
