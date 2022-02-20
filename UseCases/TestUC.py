import numpy as np
from PIL import Image

from Entities.ShiftingArray import ShiftingArray


class TestUC:
    def __init__(self, data, selectedProcessingStrategy, selectedEvaluatingStrategies):
        self.inputFrames = data
        self.processingStrategy = selectedProcessingStrategy
        self.evaluatingStrategies = selectedEvaluatingStrategies

        self.outputFrames = data.copy()

    def getFrameAt(self, index):
        return self.outputFrames[index]

    def updateData(self, selectedData):
        self.inputFrames = selectedData
        self.outputFrames = selectedData.copy()
        self.calculate()

    def updateSettings(self, selectedProcessingStrategy, selectedEvaluatingStrategies):
        self.processingStrategy = selectedProcessingStrategy
        self.evaluatingStrategies = selectedEvaluatingStrategies
        self.calculate()

    def calculate(self):
        strategy = self.processingStrategy
        processingOutLen = len(self.inputFrames) - (strategy.frameCount - 1)
        processingResults = ShiftingArray(None, maxCount=processingOutLen)

        resizedFrames = list()
        cameraResolution = (self.inputFrames[0].shape[1], self.inputFrames[0].shape[0])
        resizedResolution = (
            int(cameraResolution[0] / self.processingStrategy.frameDivider),
            int(cameraResolution[1] / self.processingStrategy.frameDivider)
        )

        for frame in self.inputFrames:
            imgBuffer = Image.fromarray(frame, 'RGB')
            imgBuffer = imgBuffer.resize(resizedResolution)
            resizedFrames.append(np.array(imgBuffer))


        for i in range(processingOutLen):
            usedFrames = resizedFrames[i:i+strategy.frameCount]
            processingResults.push(strategy.calculate(usedFrames))

        evalStrategies = self.evaluatingStrategies
        for i in range(processingOutLen):
            frame = self.inputFrames[i].copy()
            for evalStrategy in evalStrategies:
                neededPoints = evalStrategy.dataPoints
                availablePoints = i
                if neededPoints <= availablePoints:
                    evalData = processingResults.get()
                    evalData.reverse()
                    evalData = evalData[i-neededPoints:i]
                    evalData.reverse()
                    frame = evalStrategy.evaluate(frame, evalData, [None]*neededPoints)
            self.outputFrames[i] = frame

