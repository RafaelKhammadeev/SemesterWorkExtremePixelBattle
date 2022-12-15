import socket
from time import sleep
import datetime
from threading import Thread

import pickle


# происходит подключение пользовать
class ConnectedClient(Thread):
    def __init__(self, server, client_socket):
        super().__init__()
        self.sock = client_socket
        self.server = server
        self.client_online = True

    def run(self):
        while 1:
            info = self.recv()

            # если клиент онлайн
            if self.client_online:
                msg = info.get('text')
                from_name = info.get('from')
                date = info.get('when')
                text = f"[{from_name}][{date}]::{msg}"
                self.server.send_all_client(text)

    def send(self, text):
        protocol = {"text": text,
                    "from": 'kek',
                    "when": datetime.datetime.now()}
        self.sock.send(pickle.dumps(protocol))

    def recv(self):
        if self.client_online:
            obj = self.sock.recv(1024)

            # обработка при выходе (при выходе возвращает нулевые байты)
            if obj is None or not len(obj):
                self.client_online = False
                self.server.send_all_client("Клиент вышел фольдсвагинпасад")
                Server.delete_client(self.sock)
                self.sock.close()
                return

            info = pickle.loads(obj)
            return info


# Todo поле должно находиться в сервере
#  ну и где то получать значения
# сервер
class Server:
    CLIENTS = set()

    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # re-open port if busy
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.listen(5)

    def send_all_client(self, text):
        for client_data in Server.CLIENTS:
            client = client_data[0]
            client.send(text)

    def start_server(self):
        while 1:
            # ждет подключение клиента
            client_socket, (ip, port) = self.sock.accept()
            print(f"Client ip={ip} [{port}] connected")
            connected_client = ConnectedClient(self, client_socket)

            # начала работы клиента
            connected_client.start()

            # client_data хранит в себе клиентский сокет и его соединение
            client_data = (connected_client, client_socket)
            Server.CLIENTS.add(client_data)
            # welcome msg because argument list is empty
            self.send_all_client(f"К нам подключился {ip} [{port}]")

    @staticmethod
    def delete_client(client):

        for client_data in Server.CLIENTS:
            client_socket = client_data[1]

            if client_socket == client:
                Server.CLIENTS.remove(client_data)
                break


address = ("localhost", 10000)
server = Server(address)
server.start_server()
