import os
import pickle
import sys
from PyQt5.QtWidgets import QApplication


from Entities.ProcessingStrategy import *
from Entities.EvaluationStrategy import *
from .View import View
from .Model import Model


class Controller:
    view: View
    model: Model

    allProcessingStrategies = (
        ProcessingStrategy1("fD = 64", frameDivider=64),
        ProcessingStrategy1("fD = 128", frameDivider=128)
    )
    allEvaluatingStrategies = (
        currentFPSandDT(),
        averageFPSandDT(),
        showCurrentPositions()
    )

    def __init__(self):
        self.processingStrategies = {str(processingStrategy): processingStrategy
                                     for processingStrategy in self.allProcessingStrategies}
        self.selectedProcessingStrategy = self.allProcessingStrategies[0]
        self.evaluationStrategies = {str(evaluatingStrategy): evaluatingStrategy
                                     for evaluatingStrategy in self.allEvaluationStrategies}
        self.selectedEvaluatingStrategies = list()


        self.testFolderPath = "TestFiles"
        self.testFileNames = os.listdir(self.testFolderPath)
        self.testFiles = dict()
        for name in self.testFileNames:
            with open(self.testFolderPath + "/" + name, "rb") as f:
                self.testFiles[name] = pickle.load(f)

        self.currentFileName = self.testFileNames[0]
        self.currentIndex = 0

        self.model = Model(
            self,
            self.allProcessingStrategies,
            self.allEvaluatingStrategies
        )

        app = QApplication(sys.argv)
        self.view = View(
            self,
            self.model,
            self.allEvaluatingStrategies,
            self.testFileNames
        )
        sys.exit(app.exec_())

    def updateView(self):
        self.view.updateView(self.model.getPictureArray())

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
