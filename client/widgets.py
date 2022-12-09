import sys
import socket
import numpy as np
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QWidget, QStackedWidget, QMessageBox, QPushButton
import typing


# виджет авторизации
class Authorization(QWidget):
    def __init__(self):
        super().__init__()
        print("The user is at the authorization stage!")

        self.nickname = None
        self.setMinimumSize(500, 500)

        uic.loadUi("design/authorization.ui", self)
        self.btn.clicked.connect(self.switch_on_lobby)

    # переключается на виджет лобби
    def switch_on_lobby(self):
        edit_label_text = self.name_text_edit.text()

        # проверка имени на длину
        if len(edit_label_text) < 4:
            self.warning_popup()
        else:

            # фиксируем никнейм пользователя
            self.nickname = edit_label_text

            lobby = Lobby()
            widget.addWidget(lobby)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    # всплывающее предупреждающее окно(alert)
    def warning_popup(self):
        alert = QMessageBox(self)
        alert.setWindowTitle("Warning")
        alert.setText("Name cannot be EMPTY and SHORTER than 4 characters")
        alert.setIcon(QMessageBox.Icon.Warning)
        # msg.setIcon(QMessageBox_Icon=Warning)
        button = alert.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("ОК!")


# виджет с лобби
class Lobby(QWidget):
    def __init__(self):
        super().__init__()
        print("User in lobby!")

        self.setMinimumSize(500, 500)

        uic.loadUi("design/lobby.ui", self)
        self.btn_lby_1.clicked.connect(self.switch_on_game)

    # переключение на виджет игры
    def switch_on_game(self):
        game = Game()
        widget.addWidget(game)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# базовый класс для всех объектов модуля
class Communication(QObject):
    # создаем свой сигнал
    dataSignal = pyqtSignal(int, int)


# Основной экран с игрой
class Game(QWidget):
    def __init__(self):
        super().__init__()
        print("User in the game!")
        self.all_buttons = []
        uic.loadUi("design/game.ui", self)

        # обработчик сигнала, связанного с объектом
        self.comm = Communication()
        self.comm.dataSignal.connect(self.change_color)

        self.init_gui()

        self.btn_exit.clicked.connect(self.switch_on_lobby)

    def init_gui(self):
        # убираем отступы у grid
        self.button_area.setSpacing(0)
        self.group_button_label.setContentsMargins(60, 0, 60, 0)

        btn_w, btn_h = 35, 35

        for i in range(30):
            for j in range(30):
                # дизайн кнопок
                btn = QPushButton()
                btn.setMaximumSize(btn_w, btn_h)
                btn.setStyleSheet("background-color : rgb(255, 255, 255);"
                                  "margin: 0px ,8px, 0px, 0px;")
                btn.clicked.connect(lambda state, x=i, y=j: self.change_color(x, y))
                print(i,j)

                self.button_area.addWidget(btn, i, j)

                self.all_buttons.append(btn)

    # переключение на виджет лобби
    @staticmethod
    def switch_on_lobby():
        lobby = Lobby()
        widget.addWidget(lobby)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    # смена цвета кнопки
    @pyqtSlot(int, int)
    def change_color(self, i, j):
        print(i, j)
        r, g, b = np.random.uniform(0, 255, 3)
        btn = self.all_buttons[i * 30 + j]
        btn.setStyleSheet(f"background-color : rgb({r}, {g}, {b})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    authorization = Authorization()
    widget.addWidget(authorization)
    widget.show()
    sys.exit(app.exec())
