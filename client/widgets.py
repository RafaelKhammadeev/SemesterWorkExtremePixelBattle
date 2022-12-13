import os
import sys
import time
import socket
import threading
import numpy as np
from PIL import Image
from PyQt6 import uic, QtTest
from datetime import datetime
# from backend_client import BackendClient
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QWidget, QStackedWidget, QMessageBox, QPushButton


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
        self.BUTTON_COUNT = 30
        self.get_signal = False

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
        self.thread_block_logic()

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

        for i in range(self.BUTTON_COUNT):
            for j in range(self.BUTTON_COUNT):
                # дизайн кнопок
                btn = QPushButton()
                btn.setMinimumSize(btn_min_w, btn_min_h)
                btn.setMaximumSize(btn_max_w, btn_max_h)
                btn.setStyleSheet("background-color : rgb(255, 255, 255);"
                                  "margin: 0px ,0px, 0px, 0px;")
                btn.clicked.connect(
                    lambda state, x=i, y=j: self.change_color(x, y))

                self.button_area.addWidget(btn, i, j)

                list_button_color = [btn, self.current_color]
                self.all_buttons.append(list_button_color)

    # Возбуждает сигналы и передает значения цвета
    def choose_color(self):
        for color_btn, color in self.colors_button.items():
            r, g, b = color
            color_btn.clicked.connect(lambda state, x=r, y=g, z=b: self.save_chosen_btn(x, y, z))

    # Сохранение цвета выбранного пользователя с палитры
    @pyqtSlot(int, int, int)
    def save_chosen_btn(self, r, g, b):
        self.current_color = r, g, b

        self.get_signal = True

        # разблокируем все кнопки
        for btn in self.all_buttons:
            btn[0].blockSignals(False)

    # смена цвета кнопки
    @pyqtSlot(int, int)
    def change_color(self, i, j):
        if self.get_signal:
            r, g, b = self.current_color

            current_button_color = self.all_buttons[i * self.BUTTON_COUNT + j]

            btn_obj = current_button_color[0]
            # нужно для запоминания цвета кнопки
            current_button_color[1] = self.current_color

            btn_obj.setStyleSheet(f"background-color : rgb({r}, {g}, {b})")

            # блокируем сигналы у всех кнопок
            for btn in self.all_buttons:
                btn[0].blockSignals(True)

    # логика thread для запуска signal_block_logic
    def thread_block_logic(self):
        print("Main    : before creating thread")
        x = threading.Thread(target=self.signal_block_for_button, daemon=True)
        print("Main    : before running thread")
        x.run()

    # подает сигнал блокировки сигнала (ну на перекрытие frame-ом)
    def signal_block_for_button(self):

        # блокирует выбор цвета, закрывает другим frame
        def block_choose_color(time_block):
            if self.get_signal:
                time_block *= 1000
                # отображается frame который, блокирует выбор цвета
                self.stackedWidget.setCurrentIndex(1)

                QtTest.QTest.qWait(time_block)

                # возвращает frame выбора цвета
                self.stackedWidget.setCurrentIndex(0)

        for btn in self.all_buttons:
            btn[0].clicked.connect(lambda state, time_block=5: block_choose_color(time_block))

    def exit_popup(self):
        button = QMessageBox.question(self, 'Question', "You really wanna to exit?",
                                      buttons=QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
                                      defaultButton=QMessageBox.StandardButton.Yes)

        if button == QMessageBox.StandardButton.Yes:
            lobby = Lobby()
            widget.addWidget(lobby)
            widget.setCurrentIndex(widget.currentIndex() - 1)

    def save_popup(self):
        button = QMessageBox.question(self, 'Question', "You wanna save this picture?",
                                      buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Save,
                                      defaultButton=QMessageBox.StandardButton.Save)

        if button == QMessageBox.StandardButton.Save:
            pixels = [btn_color[1] for btn_color in self.all_buttons]

            # делим массив на части
            array = np.array_split(pixels, self.BUTTON_COUNT, axis=0)

            # Convert the pixels into an array using numpy
            array = np.array(array, dtype=np.uint8)

            # путь папки в которой будет сохраняться
            file_image_path = "picture"
            picture_path = "image.png"

            # change format the date and time.
            curr_datetime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

            splitted_path = os.path.splitext(picture_path)

            modified_picture_path = splitted_path[0] + curr_datetime + splitted_path[1]

            # Use PIL to create an image from the new array of pixels
            new_image = Image.fromarray(array)

            # TODO в дальнейшем добавить и имя пользователя
            new_image.save(f"{file_image_path}/{modified_picture_path}")
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
