import numpy as np

from .base import IProcessingStrategy


class SimpleStrategy(IProcessingStrategy):
    name = "Not declared"

    frameDivider = 1
    frameCount = 2

    def __init__(self, name, frameDivider=32, intensityThresholdMax=240, intensityThresholdMin=220):
        self.name = f"{name} {frameDivider},{intensityThresholdMax},{intensityThresholdMin}"
        self.frameDivider = frameDivider
        self.intensityThresholdMax = intensityThresholdMax
        self.intensityThresholdMin = intensityThresholdMin

    def calculate(self, frames) -> [[float, float], [float, float], [float, float]]:
        def evaluate(pixel):
            pixelSorted = pixel.copy()
            pixelSorted.sort()
            if pixelSorted[1] == pixelSorted[2]:
                return None
            highesIndex = np.where(pixel == pixelSorted[2])
            middleIndex = np.where(pixel == pixelSorted[1])

            if pixel[middleIndex[0][0]] < self.intensityThresholdMin:
                return highesIndex[0][0]
            return None

        currentPic = np.array(frames[0]).astype(int)
        lastPic = np.array(frames[1]).astype(int)
        diffPic = currentPic - lastPic
        diffPic = np.absolute(diffPic)
        indexes = np.where((diffPic > self.intensityThresholdMax))

        pixelCount = [0, 0, 0]
        pixelIndexSum = np.zeros((3, 2))
        for i in range(len(indexes[0])):
            pixel = diffPic[indexes[0][i]][indexes[1][i]]
            retVal = evaluate(pixel)
            if retVal is not None:
                pixelCount[retVal] = pixelCount[retVal] + 1
                pixelIndexSum[retVal][0] = pixelIndexSum[retVal][0] + indexes[0][i]
                pixelIndexSum[retVal][1] = pixelIndexSum[retVal][1] + indexes[1][i]

        for i in range(3):
            if pixelCount[i] != 0:
                pixelIndexSum[i][0] = pixelIndexSum[i][0] / pixelCount[i] * self.frameDivider
                pixelIndexSum[i][1] = pixelIndexSum[i][1] / pixelCount[i] * self.frameDivider

        return pixelIndexSum
