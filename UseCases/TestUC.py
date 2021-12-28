import numpy as np
from PIL import Image

from Entities.ShiftingArray import ShiftingArray


class TestUC:
    def __init__(self, data, selectedProcessingStrategy, selectedEvaluatingStrategies):
        self.frames = data
        self.processingStrategy = selectedProcessingStrategy
        self.evaluatingStrategies = selectedEvaluatingStrategies

    def getFrameAt(self, index):
        return self.frames[index]

    def updateData(self, selectedData):
        self.frames = selectedData
        self.calculate()

    def updateSettings(self, selectedProcessingStrategy, selectedEvaluatingStrategies):
        self.processingStrategy = selectedProcessingStrategy
        self.evaluatingStrategies = selectedEvaluatingStrategies
        self.calculate()

    def calculate(self):
        strategy = self.processingStrategy
        processingOutLen = len(self.frames) - (strategy.frameCount-1)
        processingResults = ShiftingArray(None, maxCount=processingOutLen)

        resizedFrames = list()
        cameraResolution = (self.frames[0].shape[0], self.frames[0].shape[1])
        resizedResolution = (
            int(cameraResolution[0] / self.processingStrategy.frameDivider),
            int(cameraResolution[1] / self.processingStrategy.frameDivider)
        )

        for frame in self.frames:
            imgBuffer = Image.fromarray(frame, 'RGB')
            imgBuffer = imgBuffer.resize(resizedResolution)
            resizedFrames.append(np.array(imgBuffer))

        for i in range(processingOutLen):
            usedFrames = resizedFrames[i:i+strategy.frameCount]
            processingResults.push(strategy.calculate(usedFrames))

        evalStrategies = self.evaluatingStrategies
        for i in range(processingOutLen):
            frame = self.frames[i]
            for evalStrategy in evalStrategies:
                neededPoints = evalStrategy.dataPoints
                availablePoints = processingOutLen - 1 - i
                if neededPoints < availablePoints:
                    frame = evalStrategy.evaluate((frame, (processingResults.get()[i:i+neededPoints]), None))
            self.frames[i] = frame

