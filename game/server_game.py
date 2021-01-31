import threading
import socket
import pickle


class CServer(object):

    def __init__(self, serv_IP, serv_port):
        self.IP = serv_IP
        self.port = serv_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.working = True
        self.free_clients = []
        self.no_listen_clients = []
        self.clients_date = []

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
        self.no_listen_clients.append(client_join)

        thread_listening = threading.Thread(target=self.listening_client, args=())
        thread_listening.start()

        while True:  # change in the future
            # serv_date = "Hello Roma! Press F to respect 8585"
            # serv_date = bytes(serv_date, 'utf-8')
            serv_date = pickle.dumps(self.clients_date)
            client_join.send(serv_date)
            print("date_was_transformed")

            # try:
            #     result = client_join.recv(1024)
            #     # incoming_mess_time = datetime.datetime.now()
            #     # print('Incoming message', result.decode('utf-8'))
            #
            # except ConnectionResetError:
            #     print("Connection with ", client_join, " lost")
            #     break

    def listening_client(self):
        listen_client = self.no_listen_clients.pop()
        while self.working:
            try:
                client_date = listen_client.recv(1024)
                print(client_date)  # delete in the future

            except ConnectionResetError:
                print("ConnectionResetError")

            else:
                client_date_list = [listen_client, client_date]
                if len(self.clients_date) != 0:
                    for one_list in self.clients_date:
                        if one_list.count(listen_client) != 0:
                            self.clients_date.remove(one_list)

                self.clients_date.append(client_date_list)


"""run application"""
print("*** \n[preparing for launch server]")

IP = ""  # input("IP: ")
port = int(input("port: "))

server = CServer(IP, port)
server.launch_server()
