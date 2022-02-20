import queue
from abc import ABC, abstractmethod

from PyQt5.QtCore import *

from Entities.ShiftingArray import ShiftingArray


class IPostProcessingOutput(ABC):
    @abstractmethod
    def show(self, img):
        pass


class PostProcessing:
    def __init__(self, targetFunction, trigger, maxCount=50):
        super().__init__()
        self.targetFunction = targetFunction
        self.trigger = trigger
        self.threads = queue.Queue()
        self.strategies = None
        self.maxCount = maxCount

    def run(self):
        while self.threads.empty():
            pass
        thread = self.threads.get()
        thread.join()
        storage = ShiftingArray(thread, maxCount=self.maxCount)

        # fill buffer
        while not storage.full():
            while self.threads.empty():
                pass
            thread = self.threads.get()
            thread.join()
            storage.push(thread)

        while True:
            while not self.threads.empty():
                thread = self.threads.get()
                thread.join()
                outputFrame = thread.currentFrame
                storage.push(thread)

                if self.strategies is not None:
                    for strategy in self.strategies:
                        if strategy.dataPoints > self.maxCount:
                            print("strategy has too many dataPoints")
                            print(strategy)
                        else:
                            outputFrame = strategy.evaluate(storage.get()[0, strategy.dataPoints], outputFrame)
                    self.trigger.emit(outputFrame)


class QPostProcessing(QThread):
    trigger = pyqtSignal()

    def __init__(self, targetFunction, maxCount=50):
        super(QPostProcessing, self).__init__()
        self.post = PostProcessing(maxCount, self.trigger)
        self.trigger.connect(targetFunction)

    def run(self):
        self.post.run()

    def dataInput(self, result):
        self.post.threads.put(result)
