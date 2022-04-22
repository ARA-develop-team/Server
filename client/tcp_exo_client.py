import socket

IP = '147.175.115.34'
port = 777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, port))

run = True

while run:
    result = sock.recv(1024)
    print(result)

    answer = input()
    if answer == '%%':
        break
    # answer = bytes(answer, 'utf-8')
    sock.send(answer)


sock.close()

# while run:
#     number += 1
#     mess = bytes(str(number), 'utf-8')
#     sock.send(mess)
# sock.close()
