import socket
from PyQt6.QtCore import QThread

import pickle
import datetime


class BackendClient(QThread):
    address = ("localhost", 10000)

    def __init__(self, signal, name):
        super().__init__()
        self.name = name
        self.signal = signal

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(BackendClient.address)

    def run(self):
        while 1:
            binary_data = self.sock.recv(1024)
            if binary_data is None or not len(binary_data):
                break
            info = pickle.loads(binary_data)
            text = info.get('text')

            self.signal.emit(text)

    # Todo надо сделать обработку сигнала,
    #  принимать не все поле, а принимать сделанные ходы пользователем
    #  и менять основное поле которое будет крутиться в main thread
    def send(self, text):
        protocol = {"text": text,
                    "from": 'kek',
                    "when": datetime.datetime.now()}
        self.sock.send(pickle.dumps(protocol))
