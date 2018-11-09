# This file handles the sudo password dialog
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import main

class PasswordWindow(QDialog):
    rejectstat = False

    def __init__(self):
        super().__init__()
        uic.loadUi('PasswordWindow.ui', self)
        print("Load password")
        self.show()

        self.rejected.connect(self.pass_reject)

    def pass_reject(self):
        self.rejectstat = True
