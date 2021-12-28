import os
import pickle
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication


from Entities.ProcessingStrategy import *
from Entities.EvaluationStrategy import *

from Controllers.Gui.View import View
from Controllers.Gui.Model import Model


class Controller:
    view: View
    model: Model

    allProcessingStrategies = [
        ProcessingStrategy1("fD = 64", frameDivider=64),
        ProcessingStrategy1("fD = 128", frameDivider=128)
    ]
    allEvaluatingStrategies = [
        currentFPSandDT(),
        averageFPSandDT(),
        showCurrentPositions()
    ]

    processingStrategies = dict()

    def __init__(self):
        # general Use
        for processingStrategy in self.allProcessingStrategies:
            self.processingStrategies[str(processingStrategy)] = processingStrategy

        self.selectedProcessingStrategy = self.allProcessingStrategies[0]
        self.evaluationStrategies = {str(evaluatingStrategy): evaluatingStrategy
                                     for evaluatingStrategy in self.allEvaluatingStrategies}
        self.selectedEvaluatingStrategies = list()

        # testing
        self.testFolderPath = "TestFiles"
        self.testFileNames = os.listdir(self.testFolderPath)
        self.testFiles = dict()
        for name in self.testFileNames:
            with open(self.testFolderPath + "/" + name, "rb") as f:
                self.testFiles[name] = pickle.load(f)

        self.currentTestFileName = self.testFileNames[0]
        self.currentTestIndex = 0

        self.model = Model(
            self.selectedProcessingStrategy,
            self.selectedEvaluatingStrategies,
            self.testFiles[self.currentTestFileName]
        )

        app = QApplication(sys.argv)
        self.view = View(
            self,
            list(self.processingStrategies.keys()),
            list(self.evaluationStrategies.keys()),
            self.testFileNames
        )
        self.view.setTestsLable(self.currentTestIndex, len(self.testFiles[self.currentTestFileName]))

        self.updateTimer = QTimer()
        self.updateTimer.setInterval(int(1 / 30))
        self.updateTimer.timeout.connect(self.updateView)
        self.updateTimer.start()
        sys.exit(app.exec_())

    def updateView(self):

        pictureArray = self.model.getPictureArray()
        self.view.setPicture(pictureArray)

    def processingChanged(self, strategyKey: str):
        self.selectedProcessingStrategy = self.processingStrategies[strategyKey]

        self.model.setSettings(self.selectedProcessingStrategy, self.selectedEvaluatingStrategies)

    def evaluationChanged(self, strategyKeys: list[str]):
        self.selectedEvaluatingStrategies = list()
        for key in strategyKeys:
            self.selectedEvaluatingStrategies.append(self.evaluationStrategies[key])

        self.model.setSettings(self.selectedProcessingStrategy, self.selectedEvaluatingStrategies)

    def testingTriggered(self, isActive):
        self.model.setTesting(
            isActive,
            self.selectedProcessingStrategy,
            self.selectedEvaluatingStrategies)

    def testingChanged(self, testKey: str):
        self.currentTestFileName = testKey
        self.currentTestIndex = 0
        self.model.setTestingIndex(self.currentTestIndex)
        self.model.testingUseCase.updateData(self.testFiles[self.currentTestFileName])
        self.view.setTestsLable(self.currentTestIndex, len(self.testFiles[self.currentTestFileName]))

    def keyPressed(self, keyNumber):
        if keyNumber.key() == Qt.Key_Right:
            if self.currentTestIndex > 0:
                self.currentTestIndex = self.currentTestIndex - 1
                self.view.setTestsLable(self.currentTestIndex, len(self.testFiles[self.currentTestFileName]))

        if keyNumber.key() == Qt.Key_Left:
            if self.currentTestIndex < len(self.testFiles[self.currentTestFileName]) - 1:
                self.currentTestIndex = self.currentTestIndex + 1
                self.view.setTestsLable(self.currentTestIndex, len(self.testFiles[self.currentTestFileName]))

        self.view.setTestsLable(self.currentTestIndex, len(self.testFiles[self.currentTestFileName]))
        self.model.setTestingIndex(self.currentTestIndex)

