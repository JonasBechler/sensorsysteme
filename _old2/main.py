import sys

from Entities.PostProcessingStrategy import *
from PyQt5.QtWidgets import QApplication

from Controllers.CamerController import CV2Controller
from Controllers.PyQtController import PyQtController
from UseCases.UseCases import *


def init():
    app = QApplication(sys.argv)

    cam = CV2Controller()
    gui = PyQtController(cam.takePicture())

    UCStart(cam, gui)
    sys.exit(app.exec_())


if __name__ == '__main__':
    init()
