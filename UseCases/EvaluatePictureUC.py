import numpy
from PyQt5.QtCore import *

from Entities.ShiftingArray import ShiftingArray


class EvaluatePicture(QObject):
    finished = pyqtSignal(numpy.ndarray)

    def __init__(self, maxCount=50):
        super().__init__()
        self.strategies = None
        self.storage = ShiftingArray((None, None, None), maxCount=maxCount)

    @pyqtSlot(tuple)
    def evaluate(self, data):
        # data = (currectFrame, result, startTime)

        if self.storage.full():
            outputFrame = data[0]
            self.storage.push(data)

            if self.strategies is not None:
                for strategy in self.strategies:
                    neededPoints = strategy.dataPoints
                    if neededPoints > self.storage.maxCount:
                        print("strategy has too many dataPoints")
                        print(strategy)
                    else:
                        outputFrame = strategy.evaluate(self.storage.get()[0:neededPoints])
            self.finished.emit(outputFrame)

        else:
            self.storage.push(data)

    @pyqtSlot(list)
    def newStrategies(self, strategies):
        self.strategies = strategies