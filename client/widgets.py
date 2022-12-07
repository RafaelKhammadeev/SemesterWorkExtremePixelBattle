import sys
import socket
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QStackedWidget, QMessageBox
import typing


# виджет авторизации
class Authorization(QWidget):
    def __init__(self):
        super().__init__()
        print("The user is at the authorization stage!")

        self.nickname = None

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

        uic.loadUi("design/lobby.ui", self)
        self.btn_lby_1.clicked.connect(self.switch_on_game)

    # переключение на виджет игры
    def switch_on_game(self):
        game = Game()
        widget.addWidget(game)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Основной экран с игрой
class Game(QWidget):
    def __init__(self):
        super().__init__()
        print("User in the game!")

        uic.loadUi("design/game.ui", self)
        self.btn.clicked.connect(self.switch_on_lobby)

    # переключение на виджет лобби
    @staticmethod
    def switch_on_lobby():
        lobby = Lobby()
        widget.addWidget(lobby)
        widget.setCurrentIndex(widget.currentIndex() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    authorization = Authorization()
    widget.addWidget(authorization)
    widget.setFixedSize(500, 500)
    widget.show()
    sys.exit(app.exec())
