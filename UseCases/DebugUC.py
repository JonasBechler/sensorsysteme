import time

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

    def updateSettings(self, selectedProcessingStrategy, selectedEvaluatingStrategies):
        self.processingStrategy = selectedProcessingStrategy
        self.takingPicture.stop()
        del self.takingPicture
        self.startTakingPictures()
        self.processingStrategy = selectedProcessingStrategy
        self.evaluationStrategyChangedSignal.emit(selectedEvaluatingStrategies)



    def __init__(self, parent, cam, updateFunction, processingStrategy):
        super().__init__()
        self.parent = parent
        self.cam = cam
        self.updateFunction = updateFunction
        self.processingStrategy = processingStrategy
        self.processingTreadsSize = 1
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
        processingThread = QThread(parent=self)
        processing.moveToThread(processingThread)

        processingThread.started.connect(processing.process)
        processing.finished.connect(self.processingFinished)

        processingThread.start()

        self.processings[self.processingIndex] = processing

        self.processingThreads[self.processingIndex].quit()
        self.processingThreads[self.processingIndex] = processingThread
        self.processingIndex = (self.processingIndex + 1) % self.processingTreadsSize

    @pyqtSlot(tuple)
    def processingFinished(self, result):
        currentFrame, result, time = result

        self.evaluationStartSignal.emit((currentFrame, result, time))


    @pyqtSlot(tuple)
    def evaluationFinished(self, outputFrame):
        self.parent.updatePicture(outputFrame)

    def __del__(self):
        self.takingPicture.stop()
        for processingThread in self.processingThreads:
            processingThread.quit()
            processingThread.running = False
        self.evaluationThread.quit()
        self.evaluationThread.running = False








