import numpy
from PyQt5.QtCore import *

from Entities.ShiftingArray import ShiftingArray


class EvaluatePicture(QObject):
    finished = pyqtSignal(numpy.ndarray)

    def __init__(self, maxCount=200):
        super().__init__()
        self.strategies = None
        self.storage = ShiftingArray((None, None), maxCount=maxCount)

    @pyqtSlot(tuple)
    def evaluate(self, data):
        # data = (currectFrame, result, startTime)

        if self.storage.full():
            currentImg = data[0]
            self.storage.push((data[1], data[2]))

            if self.strategies:
                for strategy in self.strategies:
                    neededPoints = strategy.dataPoints
                    if neededPoints > self.storage.maxCount:
                        print("strategy has too many dataPoints")
                        print(strategy)
                    else:
                        storageDatas = self.storage.get()[0:neededPoints]
                        positions = list()
                        times = list()
                        for storageData in storageDatas:
                            positions.append(storageData[0])
                            times.append(storageData[1])

                        currentImg = strategy.evaluate(currentImg, positions, times)
            self.finished.emit(currentImg)

        else:
            self.storage.push((data[1], data[2]))

    @pyqtSlot(list)
    def newStrategies(self, strategies):
        self.strategies = strategies
