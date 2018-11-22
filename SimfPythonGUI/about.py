from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
import pkg_resources


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint)
        uic.loadUi('AboutDialog.ui', self)
        self.show()
        self.versionLabel.setText(
            "Version: " +
            pkg_resources.get_distribution('SimfPythonGUI').version)
        print(str(pkg_resources.get_distribution('SimfPythonGUI').version))
