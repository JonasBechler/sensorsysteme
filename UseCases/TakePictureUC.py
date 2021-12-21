from abc import ABC, abstractmethod
from PyQt5.QtCore import *
from PIL import Image
import time
import numpy as np



from Entities.ShiftingArray import ShiftingArray

class ICameraController(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def takePicture(self):
        pass


class TakePicture(QObject):
    camera: ICameraController
    cameraResolution: (int, int)
    resizedResolution: (int, int)
    frames: ShiftingArray

    finished = pyqtSignal(list)

    def __init__(self, cam, fps, strategy):
        super(TakePicture, self).__init__()
        self.camera = cam
        self.strategy = strategy
        self.timer = QTimer()
        self.timer.setInterval(int(1000/fps))
        self.timer.timeout.connect(self._loop)

    def start(self):
        self._init()
        self.timer.start()

    def stop(self):
        self.timer.stop()


    def _init(self):
        img, time = self.camera.takePicture()

        self.cameraResolution = (img.shape[0], img.shape[1])
        self.resizedResolution = (
            int(self.cameraResolution[0] / self.strategy.frameDivider),
            int(self.cameraResolution[1] / self.strategy.frameDivider)
        )
        resizedFrameT = np.zeros(self.resizedResolution[0] * self.resizedResolution[1] * 3)
        resizedFrameT = resizedFrameT.reshape((self.resizedResolution[0], self.resizedResolution[1], 3))

        self.frames = ShiftingArray(resizedFrameT, maxCount=self.strategy.frameCount)

        while not self.frames.full():
            img, time = self.camera.takePicture()

            imgBuffer = Image.fromarray(img, 'RGB')
            imgBuffer = imgBuffer.resize(self.resizedResolution)
            self.frames.push(np.array(imgBuffer))

        return img, self.frames.get(), time

    def _loop(self):
        img, time = self.camera.takePicture()
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
        res = img, self.frames.get(), time
        res = list(res)
        self.finished.emit(res)














