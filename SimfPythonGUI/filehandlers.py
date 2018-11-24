from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene
from watchdog.events import PatternMatchingEventHandler
from datetime import date
from .config import Config


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
class ImageHandler(PatternMatchingEventHandler):
    patterns = ["*.png"]

    def __init__(self, mainwindow):
        super().__init__()
        self.main = mainwindow
        self.current = 0

        self.sceneN = QGraphicsScene()
        self.main.imgN.setScene(self.sceneN)
        self.sceneNE = QGraphicsScene()
        self.main.imgNE.setScene(self.sceneNE)
        self.sceneE = QGraphicsScene()
        self.main.imgE.setScene(self.sceneE)
        self.sceneSE = QGraphicsScene()
        self.main.imgSE.setScene(self.sceneSE)
        self.sceneS = QGraphicsScene()
        self.main.imgS.setScene(self.sceneS)
        self.sceneSW = QGraphicsScene()
        self.main.imgSW.setScene(self.sceneSW)
        self.sceneW = QGraphicsScene()
        self.main.imgW.setScene(self.sceneW)
        self.sceneNW = QGraphicsScene()
        self.main.imgNW.setScene(self.sceneNW)
        self.sceneCenter = QGraphicsScene()
        self.main.imgCenter.setScene(self.sceneCenter)

    def on_created(self, event):
        print("Update image")
        pix = QPixmap(event.src_path)

        if self.current == 0:
            self.sceneN.addPixmap(pix)
        elif self.current == 1:
            self.sceneNE.addPixmap(pix)
        elif self.current == 2:
            self.sceneE.addPixmap(pix)
        elif self.current == 3:
            self.sceneSE.addPixmap(pix)
        elif self.current == 4:
            self.sceneS.addPixmap(pix)
        elif self.current == 5:
            self.sceneCenter.addPixmap(pix)
        elif self.current == 6:
            self.sceneSW.addPixmap(pix)
        elif self.current == 7:
            self.sceneW.addPixmap(pix)
        elif self.current == 8:
            self.sceneNW.addPixmap(pix)

        self.current = (self.current + 1) % Config.dbg_lepton_set


class CSVHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]
    main = None

    def __init__(self, mainwindow):
        super().__init__()
        self.main = mainwindow

    def on_created(self, event):
        # TODO: Update irradiance count
        print("New CSV")
