import os
from configparser import SafeConfigParser
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox


class Config:
    # TODO: Comment generated config file
    config_name = 'config.ini'

    """  READ ME BEFORE EDITING BELOW
    These are the **default** values, if you want to change
    configuration values use the GUI or modify the config file named
    in the variable above and relaunch the program!
    
    If you don't have a config file, just run the program for the first
    time to generate the default file.
    """

    # paths
    lepton_grabber_working_dir = str()
    python_path = str()
    sudo_path = str()
    # Note that bash can be replaced by other compatible shells
    # All I use is echo, quit, printf, and the piping command "|"
    bash_path = str()

    # lepton-grabber launch options
    dbg_interval = int()
    dbg_png = bool()
    dbg_ffc_interval = int()
    dbg_capture_count = int()
    dbg_serial_csv = bool()
    dbg_lepton_set = int()

    @staticmethod
    def defaults():
        Config.lepton_grabber_working_dir = "lepton-grabber"
        Config.python_path = "/usr/bin/python3"
        Config.sudo_path = "sudo"
        Config.bash_path = "bash"

        Config.dbg_interval = 10
        Config.dbg_png = True
        Config.dbg_ffc_interval = -180
        Config.dbg_capture_count = 720
        Config.dbg_serial_csv = True
        Config.dbg_lepton_set = 7

    @staticmethod
    def read_config(parser):
        parser.read(Config.config_name)

        # Get Paths
        Config.lepton_grabber_working_dir = parser.get(
            'Paths', 'lepton_grabber_working_dir')
        Config.python_path = parser.get('Paths', 'python_path')
        Config.sudo_path = parser.get('Paths', 'sudo_path')
        Config.bash_path = parser.get('Paths', 'bash_path')

        # Get lepton config
        Config.dbg_interval = parser.getint('LeptonGrabberLaunchOptions',
                                            'dbg_interval')
        Config.dbg_png = parser.getboolean('LeptonGrabberLaunchOptions',
                                           'dbg_png')
        Config.dbg_ffc_interval = parser.getint('LeptonGrabberLaunchOptions',
                                                'dbg_ffc_interval')
        Config.dbg_capture_count = parser.getint('LeptonGrabberLaunchOptions',
                                                 'dbg_capture_count')
        Config.dbg_serial_csv = parser.getboolean('LeptonGrabberLaunchOptions',
                                                  'dbg_serial_csv')
        Config.dbg_lepton_set = parser.getint('LeptonGrabberLaunchOptions',
                                              'dbg_lepton_set')

    @staticmethod
    def write_config(parser):
        parser.add_section('Paths')
        parser.set('Paths', 'lepton_grabber_working_dir',
                   Config.lepton_grabber_working_dir)
        parser.set('Paths', 'python_path', Config.python_path)
        parser.set('Paths', 'sudo_path', Config.sudo_path)
        parser.set('Paths', 'bash_path', Config.bash_path)

        parser.add_section('LeptonGrabberLaunchOptions')
        parser.set('LeptonGrabberLaunchOptions', 'dbg_interval',
                   str(Config.dbg_interval))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_png',
                   str(Config.dbg_png))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_ffc_interval',
                   str(Config.dbg_ffc_interval))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_capture_count',
                   str(Config.dbg_capture_count))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_serial_csv',
                   str(Config.dbg_serial_csv))
        parser.set('LeptonGrabberLaunchOptions', 'dbg_lepton_set',
                   str(Config.dbg_lepton_set))

        with open(Config.config_name, 'w') as file:
            parser.write(file)

    def __init__(self):
        parser = SafeConfigParser(allow_no_value=True)

        if os.path.isfile(Config.config_name):
            self.read_config(parser)
        else:
            # Generate new config
            self.defaults()
            self.write_config(parser)


class ConfigEditor(QDialog):
    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint)
        uic.loadUi('SettingsDialog.ui', self)
        self.show()

        self.update_configs()

        # Init handlers
        self.buttonBox.accepted.connect(self.apply_settings)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked\
            .connect(self.apply_defaults)

    def update_configs(self):
        self.leptonWorkingDir.setText(Config.lepton_grabber_working_dir)
        self.pythonPath.setText(Config.python_path)
        self.sudoPath.setText(Config.sudo_path)
        self.shellPath.setText(Config.bash_path)

        self.capInterval.setValue(Config.dbg_capture_count)
        self.ffcInterval.setValue(Config.dbg_ffc_interval)
        self.captureCount.setValue(Config.dbg_capture_count)
        self.leptonSet.setValue(Config.dbg_lepton_set)

        self.pngEnable.setChecked(Config.dbg_png)
        self.pngDisable.setChecked(not Config.dbg_png)
        self.csvEnable.setChecked(Config.dbg_serial_csv)
        self.csvDisable.setChecked(not Config.dbg_serial_csv)

    def apply_settings(self):
        parser = SafeConfigParser(allow_no_value=True)

        # Set the settings
        Config.lepton_grabber_working_dir = self.leptonWorkingDir.text()
        Config.python_path = self.pythonPath.text()
        Config.sudo_path = self.sudoPath.text()
        Config.bash_path = self.shellPath.text()

        Config.dbg_ffc_interval = self.capInterval.value()
        Config.dbg_interval = self.capInterval.value()
        Config.dbg_capture_count = self.captureCount.value()
        Config.dbg_lepton_set = self.leptonSet.value()

        Config.dbg_png = self.pngEnable.isChecked()
        Config.dbg_serial_csv = self.csvEnable.isChecked()

        Config.write_config(parser)

    def apply_defaults(self):
        parser = SafeConfigParser(allow_no_value=True)

        Config.defaults()
        self.update_configs()
        Config.write_config(parser)
