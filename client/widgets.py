import sys
import socket
import numpy as np
import time
from PyQt6 import uic
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QWidget, QStackedWidget, QMessageBox, QPushButton, QDialogButtonBox, \
    QVBoxLayout, QLabel
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
        button = QMessageBox.warning(self, "Warning", "Name cannot be EMPTY and SHORTER than 4 characters",
                                     buttons=QMessageBox.StandardButton.Ok)

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
    # создаем свои сигналы
    dataSignal = pyqtSignal(int, int)
    colorDataSignal = pyqtSignal(int, int, int)


# Основной экран с игрой
class Game(QWidget):
    def __init__(self):
        super().__init__()
        print("User in the game!")

        # переменные
        self.all_buttons = []
        self.current_color = (255, 255, 255)

        # загрузка ui
        uic.loadUi("design/game.ui", self)

        self.colors_button = {
            self.btn_red: (255, 8, 0),
            self.btn_blue: (35, 0, 255),
            self.btn_green: (0, 194, 0),
            self.btn_black: (0, 0, 0),
            self.btn_white: (255, 255, 255),
            self.btn_orange: (255, 129, 0),
            self.btn_light_blue: (2, 212, 255),
            self.btn_yellow: (255, 251, 0),
            self.btn_purple: (135, 0, 255)
        }

        # обработчик сигнала, связанного с объектом
        self.comm = Communication()
        self.comm.dataSignal.connect(self.change_color)
        self.comm.colorDataSignal.connect(self.choose_color)

        self.init_gui()
        self.choose_color()

        self.btn_exit.clicked.connect(self.exit_popup)
        self.btn_save.clicked.connect(self.save_popup)

    # Генерирует поле кнопок, и возбуждает каждую кнопку
    def init_gui(self):
        # убираем отступы у grid
        self.button_area.setVerticalSpacing(12)
        self.button_area.setHorizontalSpacing(0)
        self.group_button_label.setContentsMargins(0, 0, 0, 0)

        btn_max_w, btn_max_h = 27, 27
        btn_min_w, btn_min_h = 20, 20

        for i in range(30):
            for j in range(30):
                # дизайн кнопок
                btn = QPushButton()
                btn.setMinimumSize(btn_min_w, btn_min_h)
                btn.setMaximumSize(btn_max_w, btn_max_h)
                btn.setStyleSheet("background-color : rgb(255, 255, 255);"
                                  "margin: 0px ,0px, 0px, 0px;")
                btn.clicked.connect(lambda state, x=i, y=j: self.change_color(x, y))

                self.button_area.addWidget(btn, i, j)

                self.all_buttons.append(btn)

    # Возбуждает сигналы и передает значения цвета
    def choose_color(self):
        for color_btn, color in self.colors_button.items():
            r, g, b = color
            color_btn.clicked.connect(lambda state, x=r, y=g, z=b: self.save_chosen_btn(x, y, z))

    # Сохранение цвета выбранного пользователя с палитры
    @pyqtSlot(int, int, int)
    def save_chosen_btn(self, r, g, b):
        self.current_color = r, g, b

    # смена цвета кнопки
    @pyqtSlot(int, int)
    def change_color(self, i, j):
        r, g, b = self.current_color
        btn = self.all_buttons[i * 30 + j]
        btn.setStyleSheet(f"background-color : rgb({r}, {g}, {b})")

    def exit_popup(self):
        button = QMessageBox.question(self, '', "You really wanna to exit?",
                                      buttons=QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
                                      defaultButton=QMessageBox.StandardButton.Yes)

        if button == QMessageBox.StandardButton.Yes:
            lobby = Lobby()
            widget.addWidget(lobby)
            widget.setCurrentIndex(widget.currentIndex() - 1)

    # TODO также должно появляться окошко (alert)
    # TODO тип с текстом вы точно хотите сохранить картинку
    # TODO и с двумя кнопками сохранить и отмена
    # TODO если нажать на кнопку сохранить, то должно произойти сохранение
    # TODO через pilow, думаю сохранять картинки будем в папку picture
    # TODO ну кнопка отмена просто возвращает обратно
    def save_popup(self, event):
        button = QMessageBox.question(self, '', "You wanna save this picture?",
                                      buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Save,
                                      defaultButton=QMessageBox.StandardButton.Save)

        if button == QMessageBox.StandardButton.Save:
            print("Save")
        else:
            print("Cancel")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    authorization = Authorization()
    widget.addWidget(authorization)
    widget.show()
    sys.exit(app.exec())
