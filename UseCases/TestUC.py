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
        for i in range(processingOutLen):
            processingResults.push(strategy.calculate(self.frames[i:i+strategy.frameCount]))

        evalStrategies = self.evaluatingStrategies
        for i in range(processingOutLen):
            frame = self.frames[i]
            for evalStrategy in evalStrategies:
                neededPoints = evalStrategy.dataPoints
                availablePoints = processingOutLen - 1 - i
                if neededPoints < availablePoints:
                    frame = evalStrategy.evaluate(frame, processingResults.get()[i:i+neededPoints], None)
            self.frames[i] = frame

