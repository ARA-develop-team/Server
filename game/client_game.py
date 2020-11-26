import pickle
import socket
import threading


class CClient(object):

    def __init__(self, serv_IP, serv_port):
        self.IP = serv_IP
        self.port = serv_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.working = True
        self.my_date = []
        self.serv_date = []

    def connection_to_server(self):
        self.sock.connect((self.IP, self.port))

        thread_listening = threading.Thread(target=self.listening_serv, args=())
        thread_transmission = threading.Thread(target=self.transmission_to_server, args=())
        thread_listening.start()
        thread_transmission.start()

    def listening_serv(self):
        while self.working:
            self.serv_date = self.sock.recv(1024)
            print(self.serv_date)   # delete in the future

    def transmission_to_server(self):
        while self.working:
            my_date = pickle.dumps(self.my_date)
            # my_date = bytes(self.my_date, 'utf-8')
            self.sock.send(my_date)


# IP = '176.38.153.161'   # input("IP: ")
# port = 8585  # int(input("port: "))
#
# client = CClient(IP, port)
# client.connection_to_server()
# IP = 1   # input("IP: ")
# port = 1  # int(input("port: "))
#
# client = CClient(IP, port)
# client.connection_to_server()

#     result = sock.recv(1024)
#     print(result)
#     mess = input('')
#     mess = bytes(mess, 'utf-8')
#     sock.send(mess)
# sock.close()
