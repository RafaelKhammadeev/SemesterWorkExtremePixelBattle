import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QMessageBox, QDialogButtonBox)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        reply = QDialogButtonBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No, QDialogButtonBox.StandardButton.No)

        if reply == QDialogButtonBox.StandardButton.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = MainWindow()
    demo.show()

    sys.exit(app.exec())
