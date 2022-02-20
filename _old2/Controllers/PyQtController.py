import PIL.Image
from Entities.PostProcessingStrategy import *
from Entities.ProcessingStrategy import *
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PyQtController(QWidget):
    def __init__(self, startPicture):
        ProcessingStrategies = ProcessingStrategy1
        PostProcessingStrategies = (currentFPSandDT(), averageFPSandDT())

        super().__init__()
        self.setWindowTitle("QPixmap Demo")

        # self.pictureQueue.put(self.cam.takePicture())
        # while self.pictureQueue.empty():
        #     pass
        img = startPicture
        size = (img.shape[1] + 200, img.shape[0])
        self.setFixedSize(size[0], size[1])

        self.pictureOutput = QLabel()
        Qimg = ImageQt(PIL.Image.fromarray(startPicture))
        self.pictureOutput.setPixmap(QPixmap.fromImage(Qimg))

        settingsInput = self.settingsInput(ProcessingStrategies, PostProcessingStrategies)

        layout = QHBoxLayout()
        layout.addWidget(self.pictureOutput)
        layout.addWidget(settingsInput)
        self.setLayout(layout)
        self.show()

    def updatePicture(self):
        if self.uiConnection.outputQueue.empty() is False:
            Qimg = ImageQt(PIL.Image.fromarray(self.uiConnection.outputQueue.get()))
            self.pictureOutput.setPixmap(QPixmap.fromImage(Qimg))

    class settingsInput(QWidget):
        def __init__(self, processingStrategies, postProcessingStrategies):
            super().__init__()
            layout = QVBoxLayout()

            processingStrategieText = QLabel()
            processingStrategieText.setText("Select Postprocessingstrategies")
            processingStrategieText.setAlignment(Qt.AlignCenter)
            processingStrategieText.setFixedHeight(30)
            layout.addWidget(processingStrategieText)

            self.processingStrategiesCombobox = QComboBox()
            self.processingStrategies = {str(processingStrategies): processingStrategies}
            self.processingStrategiesCombobox.addItems(self.processingStrategies.keys())
            self.processingStrategiesCombobox.currentIndexChanged.connect(self.processingChanged)
            layout.addWidget(self.processingStrategiesCombobox)

            postProcessingStrategieText = QLabel()
            postProcessingStrategieText.setText("Select Postprocessingstrategies")
            postProcessingStrategieText.setFixedHeight(30)
            layout.addWidget(postProcessingStrategieText)

            self.postProcessingStrategies = {}
            for i, postProcessingStrategie in enumerate(postProcessingStrategies):
                self.postProcessingStrategies[str(postProcessingStrategie)] = (
                postProcessingStrategie, QCheckBox(str(postProcessingStrategie)))
                self.postProcessingStrategies[str(postProcessingStrategie)][1].stateChanged.connect(
                    lambda: self.postProcessingChanged())
                layout.addWidget(self.postProcessingStrategies[str(postProcessingStrategie)][1])

            layout.addWidget(QWidget())
            self.setLayout(layout)
            self.show()

        def processingChanged(self):
            strategy = self.processingStrategiesCombobox.currentText()
            return self.processingStrategies[strategy]

        def postProcessingChanged(self):
            allStrategies = self.postProcessingStrategies
            strategies = []
            for key, value in allStrategies.items():
                if value[1].isChecked():
                    strategies.append(value[0])
            return strategies
