from .base import IProcessingStrategy


class TestStrategy(IProcessingStrategy):
    name = "test"

    frameDivider = 32
    frameCount = 2

    strengthThreshold = [100, 100, 100]
    countThreshold = [5, 5, 5]

    def __init__(self, name, frameDivider=32, strengthThreshold=None, countThreshold=None):
        self.name = name
        self.frameDivider = frameDivider
        if strengthThreshold is not None:
            self.strengthThreshold = strengthThreshold
        if countThreshold is not None:
            self.countThreshold = countThreshold

    def calculate(self, frames):

        frameDifference = frames[0] - frames[1]
        pixelsCount = [0, 0, 0]
        pixelsSum = [[0, 0], [0, 0], [0, 0]]
        for y in range(frameDifference.shape[0] - 1):
            for x in range(frameDifference.shape[1] - 1):
                pixel = frameDifference[y, x, :]
                for i in range(3):
                    if abs(pixel[i]) > self.strengthThreshold[i]:
                        pixelsCount[i] = pixelsCount[i] + 1
                        pixelsSum[i][0] = pixelsSum[i][0] + x
                        pixelsSum[i][1] = pixelsSum[i][1] + y

        for i in range(3):
            if pixelsCount[i] < self.countThreshold[i]:
                pixelsSum[i] = [None, None]
            else:
                pixelsSum[i] = [int(pixelsSum[i][0] * self.frameDivider / pixelsCount[i]),
                                int(pixelsSum[i][1] * self.frameDivider / pixelsCount[i])]

        return pixelsSum
