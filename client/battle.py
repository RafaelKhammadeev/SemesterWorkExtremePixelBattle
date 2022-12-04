import sys
import socket
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QStackedWidget


class Main(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/screen1.ui", self)
        self.button.clicked.connect(self.gotoScreen2)

    def gotoScreen2(self):
        screen2 = Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Screen2(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("design/screen2.ui", self)
        self.button.clicked.connect(self.gotoScreen1)

    def gotoScreen1(self):
        main = Main()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()-1)
        print("widget")


app = QApplication(sys.argv)
widget = QWidget()
widget = QStackedWidget()
main = Main()
screen2 = Screen2()
widget.addWidget(main)
widget.addWidget(screen2)
widget.setFixedSize(500, 500)
widget.show()
sys.exit(app.exec())
