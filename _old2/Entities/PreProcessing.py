import time
import threading
import sys
import numpy as np
from PIL import Image
from abc import ABC, abstractmethod
from PyQt5.QtCore import *

from Entities.Processing import QProcessing
from Entities.ProcessingStrategy import IProcessingStrategy
from Entities.ShiftingArray import ShiftingArray

from TestSamples.SampleAccess import SampleAccess


class ICameraController(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def takePicture(self):
        pass


class PreProcessing(SampleAccess):
    def __init__(self, strategy: IProcessingStrategy, camera: ICameraController, targetDeltaT=1/30):
        super().__init__()
        self.strategy = strategy
        self.camera = camera
        self.targetDeltaT = targetDeltaT

        self.cameraResolution = None
        self.resizedResolution = None
        self.frames = None

    def run(self):
        self.init()

        while True:
            self.loop()

    def init(self):
        img = self.camera.takePicture()

        self.cameraResolution = [img.shape[0], img.shape[1]]
        self.resizedResolution = (
            int(self.cameraResolution[0] / self.strategy.frameDivider),
            int(self.cameraResolution[1] / self.strategy.frameDivider)
        )
        resizedFrameT = np.zeros(self.resizedResolution[0] * self.resizedResolution[1] * 3)
        resizedFrameT = resizedFrameT.reshape((self.resizedResolution[0], self.resizedResolution[1], 3))

        self.frames = ShiftingArray(resizedFrameT, maxCount=self.strategy.frameCount)

        while not self.frames.full():
            img = self.camera.takePicture()

            imgBuffer = Image.fromarray(img, 'RGB')
            imgBuffer = imgBuffer.resize(self.resizedResolution)
            self.frames.push(np.array(imgBuffer))

        return img, self.frames.get(), self.strategy, time.time()

    def loop(self):

        img = self.camera.takePicture()
        imgBuffer = Image.fromarray(img, 'RGB')
        imgBuffer = imgBuffer.resize(self.resizedResolution)
        self.frames.push(np.array(imgBuffer))

        # folder = "ProcessingStrategyInput/x2/none/"
        # if self.getFileCount(folder) < 50:
        #     self.saveSample(folder, (img, self.frames.get()))
        # else:
        #     pass
        # print(self.getFileCount(folder))
        #
        return img, self.frames.get(), self.strategy, time.time()


class QPreProcessing(QThread):
    def __init__(self, strategy: IProcessingStrategy, camera: ICameraController, targetFunction, targetFPS=30, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.targetFunction = targetFunction
        self.pre = PreProcessing(strategy, camera)
        img, frames, strategy, currentTime = self.pre.init()
        processingThreadT = QProcessing(img, frames, strategy, time, self.targetFunction)
        self.threads = ShiftingArray(processingThreadT)

        self.targetDeltaT = int(1/targetFPS*1000)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.PreProcessingLoop)



    def PreProcessingLoop(self):
        img, frames, strategy, currentTime = self.pre.loop()
        thread = QProcessing(img, frames, strategy, time, self.targetFunction)
        thread.start()
        self.threads.push(thread)


    def run(self):

        self.timer.start(100)  # int(1000/self.targetDeltaT))
        loop = QEventLoop()
        loop.exec_()






