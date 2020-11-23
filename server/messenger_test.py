import threading
import socket
import datetime


class CServer(object):

    def __init__(self, serv_IP, serv_port):
        self.IP = serv_IP
        self.port = serv_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.working = True
        self.free_clients = []

    def launch_server(self):
        self.sock.bind((self.IP, self.port))
        self.sock.listen(5)

        print("[server is running]")
        thread_expectation = threading.Thread(target=self.expectation_of_clients, args=())
        thread_expectation.start()

    def expectation_of_clients(self):  # waiting for new connection
        while self.working:
            try:
                client, addr = self.sock.accept()

            except KeyboardInterrupt:
                self.sock.close()
                print("KeyboardInterrupt")
                self.working = False

            else:
                self.free_clients.append(client)
                client.send(b"Welcome")
                print("Connection with ", client, addr)
                if len(self.free_clients) != 0:
                    thread_working_client = threading.Thread(target=self.work_with_client, args=())
                    thread_working_client.start()

    def work_with_client(self):
        client_join = self.free_clients.pop()

        while True:     # change in the future
            try:
                result = client_join.recv(1024)
                mess_time = datetime.datetime.now()
                print('Incoming message', result.decode('utf-8'))

            except ConnectionResetError:
                print("Connection with ", client_join, " lost")
                break


"""run application"""
print("*** \n[preparing for launch server]")

IP = input("IP: ")
port = int(input("port: "))

server = CServer(IP, port)
server.launch_server()
