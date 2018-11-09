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
import sudo

class MainWindow(QMainWindow):
    simfProcess = QProcess()
    observer = Observer()

    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)
        self.show()

        self.passprompt = None

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
        if not os.path.exists(datadir): # Wait for lepton-grabber to make the directory
            # Rather than failing here or waiting for the data directory to be created
            # Just create it ourselves
            os.mkdir(datadir)
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

    # Fired by the OK button on the sudo dialog
    def start_capture(self):
        # Retrieves the password via a QDialog
        self.passprompt = sudo.PasswordWindow()
        self.passprompt.exec_()  # Wait for the password dialog to finish
        if self.passprompt.rejectstat:  # Cancel was pressed
            return
        password = self.passprompt.passLine.text()  # Grab the password

        env = QProcessEnvironment.systemEnvironment()
        self.simfProcess.setProcessEnvironment(env)
        self.simfProcess.setWorkingDirectory("lepton-grabber")
        self.simfProcess.setProcessChannelMode(QProcess.MergedChannels)
        # Note this is a kinda hacky way to get the script to execute
        # with sudo permissions, likely a better way to do this at the system level
        self.simfProcess.start("bash")  # TODO: Make configurable
        self.simfProcess.writeData(("printf -v pw \"%q\\n\" \"" + password +"\"\n").encode('utf-8'))
        self.simfProcess.writeData(("echo $pw | sudo -S /usr/bin/python3 frame_grabber.py  --dbg_interval 10 --dbg_png --dbg_ffc_interval -180 --dbg_capture_count 720 --dbg_serial_csv 1\n").encode('utf-8'))
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
