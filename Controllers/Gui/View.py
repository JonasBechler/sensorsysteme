from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# from Controllers.Gui.Controller import Controller
import Controllers.Gui


class View(QMainWindow):
    # controller: Controller

    picture: QLabel
    settings: QWidget
    processingGroupbox: QGroupBox
    processingComboBox: QComboBox

    evaluatingGroupbox: QGroupBox
    evaluatingCheckboxes: dict[str, QCheckBox]

    testingGroupbox: QGroupBox
    testingComboBox: QComboBox

    def __init__(
            self,
            controller,
            availableProcessings: list[str],
            availableEvaluatings: list[str],
            availableTests: list[str]):
        super().__init__()
        self.controller = controller

        self.setObjectName("main")
        self.setWindowTitle("juggling")

        # picture Output
        self.picture = QLabel()
        self.picture.setObjectName("pictureOutput")
        self.picture.setFixedSize(1280, 720)


        # settings Widget
        self.settings = QWidget()
        self.settings.setObjectName("settingsInput")
        settingsLayout = QVBoxLayout()

        # settings 1
        self.processingGroupbox = QGroupBox()
        self.processingGroupbox.setObjectName("groupbox")
        self.processingGroupbox.setTitle("Processing Strategies")
        processingLayout = QVBoxLayout()
        self.processingComboBox = QComboBox()
        self.processingComboBox.addItems(availableProcessings)
        self.processingComboBox.currentIndexChanged.connect(self.processingStrategiesChanged)
        processingLayout.addWidget(self.processingComboBox)
        self.processingGroupbox.setLayout(processingLayout)
        settingsLayout.addWidget(self.processingGroupbox)

        # settings 2
        self.evaluatingGroupbox = QGroupBox()
        self.evaluatingGroupbox.setObjectName("groupbox")
        self.evaluatingGroupbox.setTitle("Evaluation Strategies")
        layout = QVBoxLayout()
        self.evaluatingCheckboxes = dict()
        for evaluation in availableEvaluatings:
            checkBox = QCheckBox(evaluation)
            checkBox.clicked.connect(self.evaluationStrategiesChanged)
            self.evaluatingCheckboxes[evaluation] = checkBox
            layout.addWidget(checkBox)
        self.evaluatingGroupbox.setLayout(layout)
        settingsLayout.addWidget(self.evaluatingGroupbox)

        # settings 3
        self.testingGroupbox = QGroupBox()
        self.testingGroupbox.setObjectName("groupbox")
        self.testingGroupbox.setTitle("Testing")
        self.testingGroupbox.setCheckable(True)
        self.testingGroupbox.setChecked(False)
        self.testingGroupbox.clicked.connect(self.testingTriggered)
        testingLayout = QVBoxLayout()
        self.testingLable = QLabel()
        self.testingLable.setText("0/n")
        testingLayout.addWidget(self.testingLable)
        self.testingComboBox = QComboBox()
        self.testingComboBox.addItems(availableTests)
        self.testingComboBox.currentIndexChanged.connect(self.testingDataChanged)
        testingLayout.addWidget(self.testingComboBox)
        self.continuousCkeckbox = QCheckBox()
        self.continuousCkeckbox.setText("Continuous")
        self.continuousCkeckbox.clicked.connect(self.testContinuousAction)
        #self.continuousRadioButton.acti
        testingLayout.addWidget(self.continuousCkeckbox)


        self.testingGroupbox.setLayout(testingLayout)
        settingsLayout.addWidget(self.testingGroupbox)

        # finish settings
        settingsLayout.addStretch(1)
        self.settings.setLayout(settingsLayout)

        # main fitting
        layout = QHBoxLayout()
        layout.addWidget(self.picture)
        layout.addWidget(self.settings)
        mainWidget = QWidget()
        mainWidget.setLayout(layout)

        self.setCentralWidget(mainWidget)
        self.show()

        self.testContinuousTimer = QTimer()
        self.testContinuousTimer.setInterval(1000/30)
        self.testContinuousTimer.timeout.connect(self.testContinuous)

    def testContinuous(self):
        self.controller.keyPressed(Qt.Key_Left)

    def testContinuousAction(self):
        if self.continuousCkeckbox.isChecked():
            self.testContinuousTimer.start()
        else:
            self.testContinuousTimer.stop()


    def keyPressEvent(self, e):
        self.controller.keyPressed(e.key())

    # used by Controller
    def setPicture(self, pictureArray):

        try:
            h, w, ch = pictureArray.shape
            bytes_per_line = ch * w
            image = QImage(pictureArray.data, w, h, bytes_per_line, QImage.Format_RGB888)
            image = QPixmap.fromImage(image)


            #image = image.scaled(QSize(w * 32, h * 32))
            self.picture.setPixmap(image)
        except:
            pass

    def setAvailableProcessings(self, strategies: list[str]) -> None:
        self.processingComboBox.clear()
        self.processingComboBox.addItems(strategies)
        self.processingComboBox.currentIndexChanged.connect(self.processingStrategiesChanged)

    def setAvailableEvaluationes(self, evaluations: list[str]) -> None:
        layout = QVBoxLayout()
        for evaluation in evaluations:
            checkBox = QCheckBox(evaluation)
            checkBox.clicked.connect(self.evaluationStrategiesChanged)
            self.evaluatingCheckboxes[evaluation] = checkBox
            layout.addWidget(checkBox)
        self.evaluatingGroupbox.setLayout(layout)

    def setAvailableTests(self, tests: list[str]) -> None:
        self.testingComboBox.clear()
        self.testingComboBox.addItems(tests)

    def setTestsLable(self, currentIndex, maxIndex) -> None:
        self.testingLable.setText(str(currentIndex+1)+"/"+str(maxIndex))

    # on input. connects controller
    def processingStrategiesChanged(self):
        strategyKey = self.processingComboBox.currentText()
        self.controller.processingChanged(strategyKey)

    def evaluationStrategiesChanged(self):
        strategies = list()
        for evalStrategyKey in self.evaluatingCheckboxes.keys():
            if self.evaluatingCheckboxes[evalStrategyKey].checkState():
                strategies.append(evalStrategyKey)

        self.controller.evaluationChanged(strategies)

    def testingTriggered(self):
        isActive = self.testingGroupbox.isChecked()
        self.controller.testingTriggered(isActive)

    def testingDataChanged(self):
        dataKey = self.testingComboBox.currentText()
        self.controller.testingChanged(dataKey)

    def closeEvent(self, event):
        self.controller.close()
        event.accept()
