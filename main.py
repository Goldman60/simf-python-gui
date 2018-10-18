#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('button', self)
        btn.setToolTip('I am a button!')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(400, 400, 400, 200)
        self.setWindowTitle('SIMF GUI')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
