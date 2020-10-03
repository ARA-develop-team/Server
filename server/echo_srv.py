import socket

server = True
IP = input()
port = int(input())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP, port))
sock.listen(5)

print("Server is running")

while server:
    try:
        client, addr = sock.accept()
    except KeyboardInterrupt:
        sock.close()
        break
    else:
        client.send(b"Welcome")
        print("Connection with ", client, addr)
        while server:
            try:
                result = client.recv(1024)
            except ConnectionResetError:
                print("Connection with ", client, addr, " lost")
                break
            else:
                print('Incoming message', result.decode('utf-8'))
                ans = input()
                ans = bytes(ans, 'utf-8')
                client.send(ans)


#         print(str(result))
#         if str(result) == "b'quit'":
#             server = False
# sock.close()
