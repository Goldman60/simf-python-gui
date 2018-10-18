#!/usr/bin/env python
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

#TODO: https://stackoverflow.com/questions/22069321/realtime-output-from-a-subprogram-to-stdout-of-a-pyqt-widget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)
        self.show()

        # Register Events
        self.startCapButton.clicked.connect(self.start_capture)
        self.stopCapButton.clicked.connect(self.stop_capture)

    def start_capture(self):
        print('Start capture')

    def stop_capture(self):
        print('Stop capture')


# Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
