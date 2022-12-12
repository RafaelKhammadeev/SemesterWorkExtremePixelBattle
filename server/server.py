import socket
from time import sleep
import datetime
from threading import Thread

import pickle


class ConnectedClient(Thread):
    def __init__(self, server, client_socket, ip, port):
        super().__init__()
        self.sock = client_socket
        self.server = server
        self.ip = ip
        self.port = port

    def run(self):
        while 1:
            info = self.recv()
            msg = info.get('text')
            from_name = info.get('from')
            date = info.get('when')
            text = f"[{from_name}][{date}]::{msg}"
            self.server.send_all(text)

    def send(self, text):
        protocol = {"text": text,
                    "from": 'kek',
                    "when": datetime.datetime.now()}
        self.sock.send(pickle.dumps(protocol))

    def recv(self):
        obj = self.sock.recv(1024)
        info = pickle.loads(obj)
        return info


class Server:
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # re-open port if busy
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.listen(3)
        self.clients = set()

    def send_all(self, text):
        for client in self.clients:
            client.send(text)

    def start_server(self):
        while 1:
            client_socket, (ip, port) = self.sock.accept()
            print(f"Client ip={ip} [{port}] connected")
            connected_client = ConnectedClient(self, client_socket, ip, port)
            connected_client.start()
            self.clients.add(connected_client)
            # welcome msg because argment list is empty
            self.send_all(f"К нам подключился {ip} [{port}]")


address = ("127.0.0.1", 10000)
server = Server(address)
server.start_server()
