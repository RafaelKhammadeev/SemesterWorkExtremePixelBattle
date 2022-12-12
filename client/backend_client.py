import sys
import socket
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThread

import pickle
import datetime


class BackendClient(QThread):
    address = ("127.0.0.1", 10000)

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
            print(binary_data)
            info = pickle.loads(binary_data)
            #
            print(info)
            text = info.get('text')
            data = info.get('data')  # for example

            self.signal.emit(text)

    def send(self, text):
        protocol = {"text": text,
                    "from": 'kek',
                    "when": datetime.datetime.now()}
        self.sock.send(pickle.dumps(protocol))


class Main(QMainWindow):
    msg_signal = pyqtSignal(str)

    def __init__(self, name):
        super().__init__()

        self.second_screen = None
        self.name = name
        self.msg_signal.connect(self.recv_msg)

        self.client = BackendClient(self.msg_signal, name)
        self.client.start()

        self.gui()
        self.logic()

    def gui(self):
        self.chat_area: QTextEdit

        uic.loadUi('chat.ui', self)

        self.show()

    def logic(self):
        self.findChild(QPushButton, 'btn_send').clicked.connect(self.send_msg)
        self.btn_clear.clicked.connect(self.clear_area)
        self.chat_area.setText("Welcome fgdghggh")

    @pyqtSlot(str)
    def recv_msg(self, text):
        self.chat_area.append(text)

    def clear_area(self):
        self.chat_area.setText("")
        # prekol
        # self.second_screen = QWidget()
        # self.second_screen.show()

    def send_msg(self):
        text: str = self.input_area.text()
        if len(text.strip()) > 0:
            self.input_area.setText("")
            # socket
            self.client.send(text)


app = QApplication(sys.argv)

name = 'rafael'
main = Main(name)
sys.exit(app.exec())
