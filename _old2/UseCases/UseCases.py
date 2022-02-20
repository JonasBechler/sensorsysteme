from Entities.PostProcessing import *
from Entities.PreProcessing import *
from Entities.ProcessingStrategy import *
from PyQt5.QtCore import *


# the user starts the program
class UCStart(QObject):
    def __init__(self, camera, gui):
        # ucSeePicture = UCSeePicture(gui.updatePicture)
        QObject.__init__(self)
        # self.postThread = QPostProcessing(ucSeePicture.show, maxCount=50)
        self.preThread = QPreProcessing(ProcessingStrategy1(), camera, self.test)  # , self.postThread.dataInput)
        self.preThread.start()

    def test(self, *args):
        print("works")


# The app shows the uses the picture and how good he can juggle
class UCSeePicture(QObject):
    trigger = pyqtSignal()

    def __init__(self, targetFunction):
        super(UCSeePicture, self).__init__()
        self.trigger.connect(targetFunction)

    def show(self, img):
        self.trigger.emit(img)
