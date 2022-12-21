import os
import sys
import threading
import time

import numpy as np
from PIL import Image
from datetime import datetime
from PyQt6 import uic, QtTest
# from config import BUTTON_COUNT
# from server.server import Server
from backend_client import BackendClient
from PyQt6.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QMainWindow

# данные с конфиг, вынес сюда тк не получается запустить без него
BUTTON_COUNT = 30


# виджет авторизации
class Authorization(QMainWindow):
    def __init__(self):
        super().__init__()
        print("The user is at the authorization stage!")

        self.nickname = None
        # для чего сохраняем?
        self.lobby_widget = None
        self.setMinimumSize(500, 500)

        uic.loadUi("design/authorization.ui", self)
        self.btn.clicked.connect(self.switch_on_lobby)
        self.show()

    # переключается на виджет лобби
    def switch_on_lobby(self):
        edit_label_text = self.name_text_edit.text()

        # проверка имени на длину
        if len(edit_label_text) < 4:
            self.warning_popup()
        else:

            # фиксируем никнейм пользователя
            self.nickname = edit_label_text

            self.lobby_widget = Lobby(self.nickname)
            self.lobby_widget.show()
            self.close()

    # всплывающее предупреждающее окно(alert)
    def warning_popup(self):
        button = QMessageBox.warning(self, "Warning", "Name cannot be EMPTY and SHORTER than 4 characters",
                                     buttons=QMessageBox.StandardButton.Ok)

        if button == QMessageBox.StandardButton.Ok:
            print("ОК!")


# виджет с лобби
class Lobby(QWidget):
    def __init__(self, nickname):
        super().__init__()
        print("User in lobby!")
        self.nickname = nickname

        self.game_widget = None
        self.setMinimumSize(500, 500)

        uic.loadUi("design/lobby.ui", self)
        self.btn_lby_1.clicked.connect(self.switch_on_game)

    # переключение на виджет игры
    def switch_on_game(self):
        self.game_widget = Game(self.nickname)
        self.game_widget.show()
        self.close()


# базовый класс для всех объектов модуля
class Communication(QObject):
    # создаем свои сигналы
    msg_signal = pyqtSignal(dict)
    dataSignal = pyqtSignal(int, int)
    colorDataSignal = pyqtSignal(int, int, int)


# Основной экран с игрой
class Game(QWidget):
    def __init__(self, nickname):
        super().__init__()
        print("User in the game!")

        # переменные
        self.all_buttons = []
        self.current_color = (255, 255, 255)
        self.get_signal = False
        self.nickname = nickname
        self.lobby_widget = None

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
        self.comm.msg_signal.connect(self.recv_msg)

        # Подключение Backend Client
        self.client = BackendClient(self.comm.msg_signal, self.nickname)
        self.client.start()

        # нужно чтоб поле успело передаться
        time.sleep(0.1)
        print("backend client:: generate button area")
        print(self.client.BUTTON_AREA)
        # Todo тут должен быть backend client
        #   send wno am i

        # вызов методов
        self.init_gui()
        self.choose_color()
        self.thread_block_logic()

        # обработка кнопок
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

        all_button_color = self.client.BUTTON_AREA
        current_color = 0

        for i in range(BUTTON_COUNT):
            for j in range(BUTTON_COUNT):

                # дизайн кнопок
                btn = QPushButton()
                btn.setMinimumSize(btn_min_w, btn_min_h)
                btn.setMaximumSize(btn_max_w, btn_max_h)

                btn_color = all_button_color[current_color]
                btn.setStyleSheet(f"background-color : rgb{btn_color};"
                                  "margin: 0px ,0px, 0px, 0px;")

                current_color += 1

                btn.clicked.connect(
                    lambda state, x=i, y=j: self.change_color(x, y))

                self.button_area.addWidget(btn, i, j)

                list_button_color = [btn, self.current_color]
                self.all_buttons.append(list_button_color)
        print(len(self.all_buttons))

    # Возбуждает сигналы и передает значения цвета
    def choose_color(self):
        for color_btn, color in self.colors_button.items():
            r, g, b = color
            color_btn.clicked.connect(lambda state, x=r, y=g, z=b: self.save_chosen_btn(x, y, z))

    # фиксирования изменения на сервере
    def send_button_color(self, coordination, color):
        print('Game:: send button color', coordination, color)
        self.client.send(coordination, color)

    # отображения появления игроков
    @pyqtSlot(dict)
    def recv_msg(self, protocol):
        coordination = protocol.get("coordination")
        color = protocol.get("color")
        text = protocol.get('text')

        if text:
            self.info_area.append(text)

        # если координация и цвет пустые, то нечего
        if not (coordination and color):
            return

        x, y = coordination

        # нужно для правильного сохранения картинки
        self.client.BUTTON_AREA[x * BUTTON_COUNT + y] = color

        current_button_color = self.all_buttons[x * BUTTON_COUNT + y]

        btn_obj = current_button_color[0]

        btn_obj.setStyleSheet(f"background-color : rgb{color}")

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

            # отлавливать изменения при нажатии и отправлять на сервер
            coordination = (i, j)
            color = r, g, b
            self.send_button_color(coordination, color)

            current_button_color = self.all_buttons[i * BUTTON_COUNT + j]

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
            self.lobby_widget = Lobby(self.nickname)
            self.lobby_widget.show()
            self.close()

    def save_popup(self):
        button = QMessageBox.question(self, 'Question', "You wanna save this picture?",
                                      buttons=QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Save,
                                      defaultButton=QMessageBox.StandardButton.Save)

        if button == QMessageBox.StandardButton.Save:
            pixels = [btn_color for btn_color in self.client.BUTTON_AREA]

            # делим массив на части
            array = np.array_split(pixels, BUTTON_COUNT, axis=0)

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
    widget = Authorization()
    sys.exit(app.exec())
