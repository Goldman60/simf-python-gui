#!/usr/bin/env python
import sys
from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QMainWindow, QApplication


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
        self.simfProcess.start("sudo python3 frame_grabber.py --dbg_interval 10 --dbg_png --dbg_ffc_interval -180 --dbg_capture_count 720 --dbg_serial_csv 1")  # TODO: Make configurable

    def stop_capture(self):
        print('Stop capture')


# TODO: Implement config file
class Config:
    def __init__(self):
        self.config = ConfigParser()

        if self.config.read('config.ini'):
            print('old config')
        else:
            print('new config')


# Main Function
if __name__ == '__main__':
    config = Config()
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
