import os

from PyQt5.QtCore import QThread, pyqtSignal
from watchdog.events import PatternMatchingEventHandler
from datetime import date
from .config import Config
from watchdog.observers import Observer


# Computes where the lepton grabber is currently dumping output
class FileHandlerUtils:
    @staticmethod
    def compute_current_data_dir():
        today = date.today()

        return Config.lepton_grabber_working_dir + "/" \
            + today.strftime("%y-%m-%d")


# TODO: This needs to be thread safe
#       Good example:
#       https://github.com/yesworkflow-org/yw-gui/blob/master/main_ui.py
class ImageThread(QThread):
    new_image = pyqtSignal(str)

    class ImageHandler(PatternMatchingEventHandler):
        patterns = ["*.png"]

        def __init__(self, event_thread):
            super().__init__()
            self.event_thread = event_thread

        def on_created(self, event):
            print("Update image")
            self.event_thread.new_image.emit(event.src_path)

    def run(self):
        datadir = FileHandlerUtils.compute_current_data_dir()

        if not os.path.exists(datadir):
            # Wait for lepton-grabber to make the directory rather than failing
            # here or waiting for the data directory to be created just create
            # it ourselves
            os.mkdir(datadir)

        observer = Observer()
        observer.schedule(self.ImageHandler(self), path=datadir)

        observer.start()
        observer.join()


# TODO: This needs to be thread safe
#       Good example:
#       https://github.com/yesworkflow-org/yw-gui/blob/master/main_ui.py
class CSVHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]
    main = None

    def __init__(self, mainwindow):
        super().__init__()
        self.main = mainwindow

    def on_created(self, event):
        # TODO: use this to determine percentage complete
        # TODO: Update irradiance count
        print("New CSV")
