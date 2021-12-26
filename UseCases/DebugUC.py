import time
import numpy as np


from PyQt5.QtCore import *

from Entities.ProcessingStrategy import IProcessingStrategy

from UseCases.TakePictureUC import TakePicture
from UseCases.ProcessPictureUC import ProcessPicture
from UseCases.EvaluatePictureUC import EvaluatePicture


class Debug(QObject):
    fps = 30

    processingStrategy: IProcessingStrategy
    evaluationStrategies = list()

    takingPicture: QObject
    processings = list()
    processingThreads = list()
    processingIndex = 0

    evaluationStartSignal = pyqtSignal(tuple)
    evaluationStrategyChangedSignal = pyqtSignal(list)
    evaluation: QObject
    evaluationThread: QThread

    picture: np.array

    def getPictureArray(self):
        return self.picture

    def updateSettings(self, selectedProcessingStrategy, selectedEvaluatingStrategies):
        self.processingStrategy = selectedProcessingStrategy
        self.takingPicture.stop()
        del self.takingPicture
        self.startTakingPictures()
        self.evaluationStrategies = selectedEvaluatingStrategies
        self.evaluationStrategyChangedSignal.emit(self.evaluationStrategies)

    def start(self):
        self.takingPicture.start()

    def stop(self):
        self.takingPicture.stop()

    def __init__(self, cam, processingStrategy):
        super().__init__()
        self.cam = cam
        self.picture = np.zeros(1280*840*3)
        self.picture.reshape((1280, 840, 3))
        self.processingStrategy = processingStrategy
        self.processingTreadsSize = 10
        self.initProcess()
        self.initEval()

        self.startTakingPictures()

    def initProcess(self):

        for i in range(self.processingTreadsSize):
            processingThread = QThread(parent=self)
            self.processingThreads.append(processingThread)
            self.processings.append(None)

    def initEval(self):
        evaluate = EvaluatePicture(maxCount=50)
        evaluateThread = QThread(parent=self)
        evaluate.moveToThread(evaluateThread)

        self.evaluationStartSignal.connect(evaluate.evaluate)
        self.evaluationStrategyChangedSignal.connect(evaluate.newStrategies)
        evaluate.finished.connect(self.evaluationFinished)

        evaluateThread.start()
        self.evaluation = evaluate
        self.evaluationThread = evaluateThread

    def startTakingPictures(self):
        takingPicture = TakePicture(self.cam, self.fps, self.processingStrategy)

        takingPicture.finished.connect(self.pictureReady)

        takingPicture.start()
        self.takingPicture = takingPicture

    @pyqtSlot(list)
    def pictureReady(self, result):

        img, resizedFrames, time = result
        processing = ProcessPicture(img, resizedFrames, self.processingStrategy, time)
        processingThread = QThread(self)
        processing.moveToThread(processingThread)

        processingThread.started.connect(processing.process)
        processing.finished.connect(self.processingFinished)

        processingThread.start()

        self.processings[self.processingIndex] = processing

        self.processingThreads[self.processingIndex].quit()
        del self.processingThreads[self.processingIndex]
        self.processingThreads.insert(self.processingIndex, processingThread)
        self.processingIndex = (self.processingIndex + 1) % self.processingTreadsSize

    @pyqtSlot(tuple)
    def processingFinished(self, result):
        currentFrame, result, time = result

        self.evaluationStartSignal.emit((currentFrame, result, time))


    @pyqtSlot(tuple)
    def evaluationFinished(self, outputFrame):
        self.picture = outputFrame

    def __del__(self):
        self.takingPicture.stop()
        for processingThread in self.processingThreads:
            processingThread.quit()
            processingThread.running = False
        self.evaluationThread.quit()
        self.evaluationThread.running = False








