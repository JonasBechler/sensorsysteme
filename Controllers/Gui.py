import time

from PyQt5 import Qt

import PIL
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QFile, QTextStream, QTimer, QRectF
from PyQt5.QtGui import QPixmap, QPicture, QImage
from PyQt5.QtWidgets import *

from Controllers.CamerController import CV2Controller
from Entities.EvaluationStrategy import *
from Entities.ProcessingStrategy import *
from UseCases.DebugUC import Debug


class PyQtController(QMainWindow):
    processingStrategies: dict
    evaluationStrategies: dict

    selectedProcessingStrategy: IProcessingStrategy
    selectedEvaluatingStrategies: list

    MAX_IMAGE_RESOLUTION = 23170

    def __init__(self):
        super().__init__()
        allProcessingStrategies = (ProcessingStrategy1("fD = 8", frameDivider=8),
                                   ProcessingStrategy1("fD = 16", frameDivider=16),
                                   ProcessingStrategy1("fD = 32", frameDivider=32),
                                   ProcessingStrategy1("fD = 64", frameDivider=64),
                                   ProcessingStrategy1("fD = 128", frameDivider=128)
                                   )
        self.processingStrategies = {str(processingStrategy): processingStrategy
                                     for processingStrategy in allProcessingStrategies}
        self.selectedProcessingStrategy = allProcessingStrategies[0]
        self.evaluationStrategies = {str(evaluatingStrategy): evaluatingStrategy
                                     for evaluatingStrategy in allEvaluationStrategies()}
        self.selectedEvaluatingStrategies = list()

        self.pixmap = None
        self.pictureOutput = None

        self.settingsInput = None

        self.mainWidget = None
        self.setupUi()
        self.useCase = Debug \
            (self,
             CV2Controller(),
             self.updatePicture,
             self.processingStrategies[list(self.processingStrategies.keys())[0]])

        self.cssTimer = QTimer()
        self.cssTimer.setInterval(500)
        self.cssTimer.timeout.connect(self.updateQSS)
        self.cssTimer.start()


    def updateQSS(self):
        file = QFile("Controllers/Gui.css")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())

    def setupUi(self):
        self.updateQSS()
        self.setObjectName("main")

        self.setWindowTitle("juggling")

        self.pictureOutput = QLabel(objectName="pictureOutput")
        # self.pictureOutput.setAutoResize(False)
        # self.pictureOutput = PhotoViewer(self)

        self.settingsInput = QWidget(objectName="settingsInput")
        settingsLayout = QVBoxLayout()
        settingsLayout.addWidget(ProzessingGroupbox(self, objectName="processing"))
        settingsLayout.addWidget(EvaluatingGroupbox(self, objectName="evaluating"))

        settingsLayout.addStretch(1)
        self.settingsInput.setLayout(settingsLayout)

        layout = QHBoxLayout()
        layout.addWidget(self.pictureOutput)
        layout.addWidget(self.settingsInput)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(layout)

        self.setCentralWidget(self.mainWidget)
        self.show()

    def updatePicture(self, pictureArray):
        h, w, ch = pictureArray.shape
        bytes_per_line = ch * w  # PEP8: `lower_case_names` for variables

        image = QImage(pictureArray.data, w, h, bytes_per_line, QImage.Format_RGB888)
        #image = image.scaled(640, 480)

        self.pictureOutput.setPixmap(QPixmap.fromImage(image))
        # Qimg = ImageQt(PIL.Image.fromarray(pictureArray))
        # self.pixmap = QPixmap.fromImage(Qimg)
        # #self.pictureOutput.setScaledContents(True)
        #
        # self.pictureOutput.setPixmap(self.pixmap)
        #
        # picture = cv2.cvtColor(pictureArray, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Juggling Tracking", picture)
        # cv2.waitKey(1)


    def updateSettings(self):
        self.useCase.updateSettings(self.selectedProcessingStrategy, self.selectedEvaluatingStrategies)

    def npArrayToQPixmap(self, picture):
        Qimg = ImageQt(PIL.Image.fromarray(picture))
        return QPixmap.fromImage(Qimg)




class ProzessingGroupbox(QGroupBox):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.setTitle("Processing Strategies")
        self.parent = parent
        self.parent.selectedProcessingStrategy = self.parent.processingStrategies[
            list(self.parent.processingStrategies.keys())[0]]
        layout = QVBoxLayout()

        self.processingStrategiesCombobox = QComboBox(objectName="processingStrategiesCombobox")
        self.processingStrategiesCombobox.addItems(self.parent.processingStrategies.keys())
        self.processingStrategiesCombobox.currentIndexChanged.connect(self.processingChanged)

        layout.addWidget(self.processingStrategiesCombobox)
        self.setLayout(layout)

    def processingChanged(self):
        strategyKey = self.processingStrategiesCombobox.currentText()
        self.parent.selectedProcessingStrategy = self.parent.processingStrategies[strategyKey]
        self.parent.updateSettings()


class EvaluatingGroupbox(QGroupBox):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.setTitle("Evaluating Strategies")
        self.parent = parent
        self.evalStrategies = self.parent.evaluationStrategies
        self.checkBoxes = dict()
        layout = QVBoxLayout()
        for evalStrategyKey in self.evalStrategies.keys():
            checkBox = QCheckBox(evalStrategyKey, objectName="evaluatingCheckBox")
            checkBox.clicked.connect(self.changed)
            self.checkBoxes[evalStrategyKey] = checkBox
            layout.addWidget(checkBox)
        self.setLayout(layout)

    def changed(self):
        strategies = list()
        for evalStrategyKey in self.evalStrategies.keys():
            if self.checkBoxes[evalStrategyKey].checkState():
                strategies.append(self.evalStrategies[evalStrategyKey])
        self.parent.selectedEvaluatingStrategies = strategies
        self.parent.updateSettings()

