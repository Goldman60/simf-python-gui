#!/usr/bin/env python
import os
import sys
import time
from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtCore import QProcess, QProcessEnvironment
from PyQt5.QtWidgets import QMainWindow, QApplication
from watchdog.observers import Observer
from filehandlers import ImageHandler, FileHandlerUtils

class MainWindow(QMainWindow):
    simfProcess = QProcess()
    observer = Observer()

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

        # Start the file observers
        if not self.observer.is_alive():
            self.observer.start()

        datadir = FileHandlerUtils.compute_current_data_dir()
        while not os.path.exists(datadir): # Wait for lepton-grabber to make the directory
            print("Waiting for data dir")
            time.sleep(3)
        self.observer.schedule(ImageHandler(self), path=datadir)

    def process_finished(self):
        self.startCapButton.setEnabled(True)
        self.stopCapButton.setDisabled(True)
        self.console_write()
        self.console_write_line("Capture Ended")

        # Unschedule the file observers while capture isn't running
        self.observer.unschedule_all()

    # Fired when the observer started in process_started
    # detects a new image from the lepton grabbers
    def update_images(self):
        self.console_write_line("New images!\n")

    # Allows the console to handle \n newlines
    def console_write_line(self, output):
        output = output.replace('\\n', '<br />')  # the QPlainTextEdit widget doesn't like newlines
        self.consoleWidget.appendHtml(output)  # So I use appendhtml and <br /> instead

    # Event handle fired when there is new stdout or stderr from SIMF
    def console_write(self):
        print('Read input!')
        output = str(self.simfProcess.readAll(), encoding='utf-8')
        self.console_write_line(output)

    # Fired when the start capture button is hit
    def start_capture(self):
        print('Start capture')
        #  TODO: get sudo password and feed it to sudo
        env = QProcessEnvironment.systemEnvironment()
        sudopw = "pw"
        self.simfProcess.setProcessEnvironment(env)
        self.simfProcess.setWorkingDirectory("lepton-grabber")
        self.simfProcess.setProcessChannelMode(QProcess.MergedChannels)
        # Note this is a kinda hacky way to get the script to execute
        # with sudo permissions, likely a better way to do this at the system level
        self.simfProcess.start("bash")  # TODO: Make configurable
        self.simfProcess.writeData(("echo " + sudopw + "| sudo -S /usr/bin/python3 frame_grabber.py  --dbg_interval 10 --dbg_png --dbg_ffc_interval -180 --dbg_capture_count 720 --dbg_serial_csv 1\n").encode('utf-8'))
        self.simfProcess.writeData("exit\n".encode('utf-8'))

    # Fired when the stop capture button is hit
    def stop_capture(self):
        self.console_write_line("Capture terminated!")
        self.simfProcess.kill()  # Kill the capture subprocess

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
