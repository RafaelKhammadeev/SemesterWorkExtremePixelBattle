import sys
import socket
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QStackedWidget
import typing


# виджет авторизации
class Authorization(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/authorization.ui", self)
        self.btn.clicked.connect(self.switch_on_lobby)

    # переключается на виджет лобби
    def switch_on_lobby(self):
        widget.addWidget(lobby)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# виджет с лобби
class Lobby(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/lobby.ui", self)
        self.btn.clicked.connect(self.switch_on_game)

    # переключение на виджет игры
    def switch_on_game(self):
        widget.addWidget(game)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # всплывающее предупреждающее окно(alert)
    # def warning_popup(self):



# Основной экран с игрой
class Game(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/game.ui", self)
        self.btn.clicked.connect(self.switch_on_lobby)

    # переключение на виджет лобби
    @staticmethod
    def switch_on_lobby():

        widget.addWidget(lobby)
        widget.setCurrentIndex(widget.currentIndex() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    authorization = Authorization()
    lobby = Lobby()
    game = Game()
    widget.addWidget(authorization)
    widget.addWidget(lobby)
    widget.addWidget(game)
    widget.setFixedSize(500, 500)
    widget.show()
    sys.exit(app.exec())
