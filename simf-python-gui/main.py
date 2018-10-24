#!/usr/bin/env python
import sys

from PyQt5 import uic
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QMainWindow, QApplication

#TODO: https://stackoverflow.com/questions/22069321/realtime-output-from-a-subprogram-to-stdout-of-a-pyqt-widget


class MainWindow(QMainWindow):
    simfProcess = QProcess()

    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)
        self.show()

        # Register Events
        self.startCapButton.clicked.connect(self.start_capture)
        self.stopCapButton.clicked.connect(self.stop_capture)

        # Process setup
        self.simfProcess.readyRead.connect(self.console_write)
        self.simfProcess.started.connect(self.process_started)
        self.simfProcess.finished.connect(self.process_finished)

    def process_started(self):
        self.startCapButton.setDisabled(True)
        self.stopCapButton.setEnabled(True)

    def process_finished(self):
        self.startCapButton.setEnabled(True)
        self.stopCapButton.setDisabled(True)

    def console_write(self):
        print('Read input!')
        output = str(self.simfProcess.readAll())
        output = output.replace('\\n', '<br />')  # the QPlainTextEdit widget doesn't like newlines
        self.consoleWidget.appendHtml(output)     # So I use appendhtml and <br /> instead

    def start_capture(self):
        print('Start capture')
        self.simfProcess.start("ls")

    def stop_capture(self):
        print('Stop capture')


# Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
