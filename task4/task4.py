import sys
import random
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtCore import pyqtSignal


class Button(QPushButton):
    mouseMoved = pyqtSignal()

    def mouseMoveEvent(self, event):
        self.mouseMoved.emit()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coords = [40, 40]
        self.btn_size = [120, 40]
        self.d = 15
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('task4')

        self.btn = Button(self)
        self.btn.setMouseTracking(True)
        self.btn.setText("Just a button")
        self.btn.move(*self.coords)
        self.btn.mouseMoved.connect(self.moveButton)
        self.show()

    def moveButton(self):
            self.coords[0] = random.randint(0, 500 - self.btn_size[0])
            self.coords[1] = random.randint(0, 400 - self.btn_size[1])
            self.btn.move(*self.coords)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
