import sys
import socket
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThread

import pickle
import datetime


class BackendClient(QThread):
    address = ("localhost", 10000)

    # address = ("", 10001)

    def __init__(self, signal):
        super().__init__()

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

    # Todo надо сделать обработку сигнала,
    #  принимать не все поле, а принимать сделанные ходы пользователем
    #  и менять основное поле которое будет крутиться в main thread
    def send(self, all_buttons):
        protocol = [all_buttons]
        self.sock.send(pickle.dumps(protocol))

#
# class Main(QMainWindow):
#     msg_signal = pyqtSignal(str)
#
#     def __init__(self, name):
#         super().__init__()
#
#         self.name = name
#         self.msg_signal.connect(self.recv_msg)
#
#         self.client = BackendClient(self.msg_signal, name)
#         self.client.start()
#
#         self.gui()
#         self.logic()
#
#     def gui(self):
#         self.chat_area: QTextEdit
#
#         uic.loadUi('/Users/rafaelkhammadeev/AllProjects/Python/python03/SemesterWorkExtremePixelBattle/chat.ui', self)
#
#         self.show()
#
#     def logic(self):
#         self.findChild(QPushButton, 'btn_send').clicked.connect(self.send_msg)
#         self.btn_clear.clicked.connect(self.clear_area)
#         self.chat_area.setText("Welcome fgdghggh")
#
#     @pyqtSlot(str)
#     def recv_msg(self, text):
#         self.chat_area.append(text)
#
#     def clear_area(self):
#         self.chat_area.setText("")
#
#     def send_msg(self):
#         text: str = self.input_area.text()
#         if len(text.strip()) > 0:
#             self.input_area.setText("")
#             # socket
#             self.client.send(text)
#
#
# app = QApplication(sys.argv)
#
# name = 'rafael'
# main = Main(name)
# sys.exit(app.exec())
