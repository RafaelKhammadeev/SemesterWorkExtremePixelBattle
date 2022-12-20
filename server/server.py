import pickle
import socket
import datetime
from config import *
from time import sleep
from threading import Thread


# TODO хочу чтоб сервер, при подкючении у нового пользователя отображалось
#   поле на котором видно клетки, которые уже были прожаты до этого
#   нужно это продумать, тип пользователь заходит и видит поле которое уже сгенерирован

# происходит подключение пользовать
class ConnectedClient(Thread):
    def __init__(self, server, client_socket, button_area):
        super().__init__()
        self.sock = client_socket
        self.server = server
        self.button_area = button_area

    def run(self):
        while 1:
            info = self.recv()
            print("recv data:: " + info)

            msg = info.get('text')
            from_name = info.get('from')
            date = info.get('when')
            text = f"[{from_name}][{date}]::{msg}"
            self.server.send_all_client(text)

    def send(self, text):
        protocol = {"text": text,
                    "from": self.name,
                    "when": datetime.datetime.now()}
        self.sock.send(pickle.dumps(protocol))

    def recv(self):
        print("Connected Client:: recv data")
        obj = self.sock.recv()

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
    BUTTON_AREA = []

    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # re-open port if busy
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.listen(5)

        # генерация поля
        self.generation_button_area(self.BUTTON_AREA)

    # инициализация игрового поля
    def generation_button_area(self, all_buttons):
        start_button_color = (255, 255, 255)
        all_count_button = BUTTON_COUNT * BUTTON_COUNT
        for i in range(all_count_button):
                all_buttons.append(start_button_color)

    def send_all_client(self, text):
        print("Server:: send all client")
        for client_data in Server.CLIENTS:
            client = client_data[0]
            client.send(text)

    def send_client(self, button_area, sock):
        print("Server:: send client")
        sock.send(pickle.dumps(button_area))

    def start_server(self):
        while 1:
            # ждет подключение клиента
            client_socket, (ip, port) = self.sock.accept()
            print(f"Client ip={ip} [{port}] connected")
            connected_client = ConnectedClient(self, client_socket, self.BUTTON_AREA)

            # начала работы клиента
            connected_client.start()

            # client_data хранит в себе клиентский сокет и его соединение
            client_data = (connected_client, client_socket)
            Server.CLIENTS.add(client_data)

            # TODO реализовать тут отправку пользователю поля, чтоб он генерировал его по нему
            self.send_client(self.BUTTON_AREA, client_socket)

            # welcome msg because argument list is empty
            self.send_all_client(f"К нам подключился {ip} [{port}]")

    @staticmethod
    def delete_client(client):

        for client_data in Server.CLIENTS:
            client_socket = client_data[1]

            if client_socket == client:
                Server.CLIENTS.remove(client_data)
                break


if __name__ == "__main__":
    address = (HOST, PORT)
    server = Server(address)
    server.start_server()
