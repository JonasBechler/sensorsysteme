import os
import pickle
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication


from Entities import Processing
from Entities import Evaluating

from Controllers.Gui.View import View
from Controllers.Gui.Model import Model


class Controller:
    view: View
    model: Model

    allProcessingStrategies = [
        Processing.FinalStrategy("final", frameDivider=16)
    ]
    allEvaluatingStrategies = [
        Evaluating.frameDivider(frameDivider=8),
        Evaluating.frameDivider(frameDivider=16),
        Evaluating.frameDivider(frameDivider=32),
        Evaluating.showSilhouette(),
        Evaluating.currentFPSandDT(),
        Evaluating.averageFPSandDT(),
        Evaluating.showCurrentPositions(),
        Evaluating.showLastNPositions(),
        Evaluating.showAveragePositions(),
        Evaluating.showAveragePositionsCoordinates(),
        Evaluating.showLastNPositionsSmooth(),
        Evaluating.speedUpDownTimes(),
        Evaluating.speedUpDownScore(),
        Evaluating.straightScore()

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

        self.currentTestFileName = self.testFileNames[0]
        self.currentTestIndex = 0
        with open(self.testFolderPath + "/" + self.currentTestFileName, "rb") as f:
            self.currentTest = pickle.load(f)

        self.model = Model(
            self.selectedProcessingStrategy,
            self.selectedEvaluatingStrategies,
            self.currentTest
        )

        self.view = View(
            self,
            list(self.processingStrategies.keys()),
            list(self.evaluationStrategies.keys()),
            self.testFileNames
        )
        self.view.setTestsLable(self.currentTestIndex, len(self.currentTest))

        self.updateTimer = QTimer()
        self.updateTimer.setInterval(int(1 / 30))
        self.updateTimer.timeout.connect(self.updateView)
        self.updateTimer.start()


    def loadTestFile(self, name):
        with open(self.testFolderPath + "/" + name, "rb") as f:
            self.currentTest = pickle.load(f)

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
        if isActive:
            self.model.debugUseCase.takingPicture.stop()
        else:
            self.model.debugUseCase.takingPicture.start()
        self.model.setTesting(
            isActive,
            self.selectedProcessingStrategy,
            self.selectedEvaluatingStrategies)


    def testingChanged(self, testKey: str):
        self.currentTestFileName = testKey
        self.loadTestFile(self.currentTestFileName)
        self.currentTestIndex = 0
        self.model.setTestingIndex(self.currentTestIndex)
        self.model.testingUseCase.updateData(self.currentTest)
        self.view.setTestsLable(self.currentTestIndex, len(self.currentTest))

    def keyPressed(self, keyNumber):
        if keyNumber == Qt.Key_Right:
            self.currentTestIndex = self.currentTestIndex - 1
            if self.currentTestIndex < 0:
                self.currentTestIndex = len(self.currentTest)-1

        if keyNumber == Qt.Key_Left:
            self.currentTestIndex = self.currentTestIndex + 1
            if self.currentTestIndex >= len(self.currentTest):
                self.currentTestIndex = 0

        self.view.setTestsLable(self.currentTestIndex, len(self.currentTest))
        self.model.setTestingIndex(self.currentTestIndex)

    def close(self):
        self.updateTimer.stop()
        self.model.close()
        sys.exit(0)
