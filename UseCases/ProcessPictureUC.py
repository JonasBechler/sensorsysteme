from PyQt5.QtCore import *


class ProcessPicture(QObject):
    finished = pyqtSignal(tuple)

    def __init__(self, currentFrame, frameResized, strategy, time):
        super().__init__()

        self.currentFrame = currentFrame
        self.framesResized = frameResized
        self.strategy = strategy
        self.time = time

    def process(self):
        result = self.strategy.calculate(self.framesResized)
        self.finished.emit((self.currentFrame, result, self.time))
