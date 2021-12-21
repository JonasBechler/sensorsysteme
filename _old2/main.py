import sys
from PyQt5.QtWidgets import QApplication

import queue


from Entities.PreProcessing import PreProcessing
from Entities.ProcessingStrategy import ProcessingStrategy1
from Entities.PostProcessing import PostProcessing
from Entities.PostProcessingStrategy import *

from UseCases.UseCases import *

from Controllers.CamerController import CV2Controller
from Controllers.PyQtController import PyQtController



def init():
    app = QApplication(sys.argv)

    cam = CV2Controller()
    gui = PyQtController(cam.takePicture())

    UCStart(cam, gui)
    sys.exit(app.exec_())




if __name__ == '__main__':
    init()
