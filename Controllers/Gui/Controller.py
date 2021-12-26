import os
import pickle
import sys

from PyQt5.QtCore import QTimer
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
        self.currentIndex = 0

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

        self.updateTimer = QTimer()
        self.updateTimer.setInterval(int(1 / 30))
        self.updateTimer.timeout.connect(self.updateView)
        self.updateTimer.start()
        sys.exit(app.exec_())

    def updateView(self):
        pictureArray = self.model.getPictureArray()
        try:
            self.view.setPicture(pictureArray)
        except:
            pass

    def processingChanged(self, strategyKey: str):
        pass

    def evaluationChanged(self, strategyKeys: list[str]):
        pass

    def testingTriggered(self, isActive: bool):
        if isActive:
            self.model.activateTesting()

        else:
            self.model.deactivateTesting()

    def testingChanged(self, testKey: str):
        self.currentFileName = testKey
