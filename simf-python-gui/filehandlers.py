from watchdog.events import PatternMatchingEventHandler
from datetime import date

# Computes where the lepton grabber is currently dumping output
class FileHandlerUtils:
    @staticmethod
    def compute_current_data_dir():
        # TODO: Implement
        today = date.today()

        return "lepton-grabber/" + today.strftime("%y-%m-%d")


class ImageHandler(PatternMatchingEventHandler):
    patterns = ["*.png"]
    main = 0

    def __init__(self, mainwindow):
        self.main = mainwindow

    def on_created(self, event):
        main.update_images()
