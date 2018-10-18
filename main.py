#!/usr/bin/python3

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow


class MainWindow:
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        app = QtWidgets.QApplication(sys.argv)
        mainwindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(mainwindow)
        mainwindow.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
