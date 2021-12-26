from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .Controller import Controller


class View(QMainWindow):
    controller: Controller

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

        # settings Widget
        self.settings = QWidget()
        self.picture.setObjectName("settingsInput")
        settingsLayout = QVBoxLayout()

        # settings 1
        self.processingGroupbox = QGroupBox()
        self.processingGroupbox.setTitle("Processing Strategies")
        processingLayout = QVBoxLayout()
        self.processingComboBox = QComboBox()
        self.processingComboBox.addItems(availableProcessings)
        self.processingComboBox.currentIndexChanged.connect(
            self.processingStrategiesChanged
        )
        processingLayout.addWidget(self.processingComboBox)
        self.processingGroupbox.setLayout(processingLayout)
        settingsLayout.addWidget(self.processingGroupbox)

        # settings 2
        self.evaluatingGroupbox = QGroupBox()
        self.evaluatingGroupbox.setTitle("Evaluation Strategies")
        layout = QVBoxLayout()
        for evaluation in availableEvaluatings:
            checkBox = QCheckBox(evaluation)
            checkBox.clicked.connect(self.evaluationStrategiesChanged)
            self.evaluatingCheckboxes[evaluation] = checkBox
            layout.addWidget(checkBox)
        self.evaluatingGroupbox.setLayout(layout)
        settingsLayout.addWidget(self.evaluatingGroupbox)

        # settings 3
        self.testingGroupbox = QGroupBox()
        self.testingGroupbox.setTitle("Testing")
        self.testingGroupbox.setCheckable(True)
        self.testingGroupbox.setChecked(False)
        self.testingGroupbox.clicked.connect(self.testingTriggered)
        testingLayout = QVBoxLayout()
        self.testingComboBox = QComboBox()
        self.testingComboBox.addItems(availableTests)
        self.testingComboBox.currentIndexChanged.connect(
            self.testingDataChanged
        )
        testingLayout.addWidget(self.testingComboBox)
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

        self.setCentralWidget(self.mainWidget)
        self.show()

    # used by Controller
    def setPicture(self, pictureArray):
        h, w, ch = pictureArray.shape
        bytes_per_line = ch * w
        image = QImage(pictureArray.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.picture.setPixmap(QPixmap.fromImage(image))

    def setAvailableProcessings(self, strategies: list[str]) -> None:
        self.processingComboBox.clear()
        self.processingComboBox.addItems(strategies)

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

    # on input. connects controller
    def processingStrategiesChanged(self) -> None:
        strategyKey = self.processingCombobox.currentText()
        self.controller.processingChanged(strategyKey)

    def evaluationStrategiesChanged(self) -> None:
        strategies = list()
        for evalStrategyKey in self.evaluatingCheckboxes.keys():
            if self.evaluatingCheckboxes[evalStrategyKey].checkState():
                strategies.append(evalStrategyKey)

        self.controller.evaluationChanged(strategies)

    def testingTriggered(self) -> None:
        isActive = self.evaluatingGroupbox.isChecked()
        self.controller.testingTriggered(isActive)

    def testingDataChanged(self) -> None:
        dataKey = self.testingGroupbox.currentText()
        self.controller.testingChanged(dataKey)
