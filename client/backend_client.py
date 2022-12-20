import pickle
import socket
import datetime
# from config import PORT, HOST
from PyQt6.QtCore import QThread

PORT = 10000
HOST = "localhost"

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
                obj = pickle.loads(obj)
                self.BUTTON_AREA += obj
                self.first_connection = False
                print(self.BUTTON_AREA)

            else:
                print("Backend Client run:: Wait Data")
                binary_data = self.sock.recv(1024)
                if binary_data is None or not len(binary_data):
                    print("Backend Client run:: Break")
                    break

                print("Backend Client run:: data", binary_data, pickle.loads(binary_data))
                info = pickle.loads(binary_data)
                text = info.get('text')

                self.signal.emit(text)

    # Todo надо сделать обработку сигнала,
    #  принимать не все поле, а принимать сделанные ходы пользователем
    #  и менять основное поле которое будет крутиться в main thread
    def send(self, text):
        protocol = {"text": text,
                    "from": self.name,
                    "when": datetime.datetime.now()}
        self.sock.send(pickle.dumps(protocol))
