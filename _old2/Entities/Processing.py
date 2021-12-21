from PyQt5.QtCore import *
import sys


class Processing:
    def __init__(self, currentFrame, frameResized, strategy, startTime):
        super().__init__()

        self.result = None
        self.currentFrame = currentFrame
        self.framesResized = frameResized
        self.strategy = strategy
        self.startTime = startTime

    def run(self):
        try:
            self.result = self.strategy.calculate(self.framesResized)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception


class QProcessing(QThread):
    trigger = pyqtSignal(list)

    def __init__(self, currentFrame, frameResized, strategy, startTime, targetFunction):
        super(QProcessing, self).__init__()
        self.processing = Processing(currentFrame, frameResized, strategy, startTime)
        self.trigger.connect(targetFunction)

    def run(self):
        self.processing.run()
        result = self.processing.result
        self.trigger.emit(result)


