import socket
import pickle
import pygame

HEADER = 64
PORT = 1
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ["!DISCONNECT", "!DISCONNECT_FROM_SERVER"]
SERVER = ""
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    # send length
    message = pickle.dumps(msg)  # packing message
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    # send message
    client.send(message)

    # reception length
    ans_length = client.recv(HEADER).decode(FORMAT)
    ans_length = int(ans_length)

    # reception message
    ans = client.recv(ans_length)
    return pickle.loads(ans)



run = True
# send([23, 56])
#
# send("!DISCONNECT")

window = pygame.display.set_mode((500, 500))
player_pos = [100, 100]
speed = 10
pygame.init()
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= speed

    if keys[pygame.K_d]:
        player_pos[0] += speed

    if keys[pygame.K_w]:
        player_pos[1] -= speed

    if keys[pygame.K_s]:
        player_pos[1] += speed

    window.fill((0, 100, 200))
    pos_player = send(player_pos)
    print(pos_player)
    for pos in pos_player:
        if pos:
            pygame.draw.circle(window, (100, 0, 0), pos, 10, 10)
    pygame.display.update()
pygame.quit()
