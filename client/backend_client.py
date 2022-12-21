import pickle
import socket
import datetime
# from config import PORT, HOST
from PyQt6.QtCore import QThread

PORT = 10000
HOST = "172.20.10.3"


class BackendClient(QThread):
    address = (HOST, PORT)
    BUTTON_AREA = []

    def __init__(self, signal, name):
        super().__init__()
        self.name = name
        self.signal = signal
        self.first_connection = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(BackendClient.address)

    def run(self):
        while 1:
            # TODO реализовать нормальное получение данных через цикл sock.recv
            if self.first_connection:
                print("Backend client get button area ::")
                obj = self.sock.recv(1024 * 16)
                self.BUTTON_AREA = pickle.loads(obj)
                self.first_connection = False
                print(self.BUTTON_AREA)
                continue

            print("Backend Client run:: Wait Data")
            binary_data = self.sock.recv(1024)

            if binary_data is None or not len(binary_data):
                print("Backend Client run:: Break")
                break

            print("Backend Client run:: data", binary_data, pickle.loads(binary_data))
            info = pickle.loads(binary_data)
            coordination = info.get("coordination")
            color = info.get("color")
            text = info.get('text')

            protocol = {"coordination": coordination,
                        "color": color,
                        "text": text}

            self.signal.emit(protocol)

    # Todo надо сделать обработку сигнала,
    #  принимать не все поле, а принимать сделанные ходы пользователем
    #  и менять основное поле которое будет крутиться в main thread
    def send(self, coordination=None, color=None, text=None):
        print("Backend Client:: send", coordination, color)
        protocol = {"coordination": coordination,
                    "color": color,
                    "text": text}
        print(pickle.dumps(protocol))
        self.sock.send(pickle.dumps(protocol))
