from abc import ABC, abstractmethod


class IProcessingStrategy(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def frameDivider(self):
        pass

    @property
    @abstractmethod
    def frameCount(self):
        pass

    @abstractmethod
    def calculate(self, frames):
        pass

    def __str__(self):
        return self.name


""" Template



from .base import IProcessingStrategy


class ProcessingStrategyName(IProcessingStrategy):
    name = "Not declared"

    frameDivider = 32
    frameCount = 2

    def __init__(self, name, frameDivider=32):
        self.name = name
        self.frameDivider = frameDivider

    def calculate(self, frames):
        frameDifference = frames[0] - frames[1]

        # CALCULATE HERE

        for i in range(3):
            if pixelsCount[i] < self.countThreshold[i]:
                pixelsSum[i] = [None, None]
            else:
                pixelsSum[i] = [int(pixelsSum[i][0] * self.frameDivider / pixelsCount[i]),
                                int(pixelsSum[i][1] * self.frameDivider / pixelsCount[i])]

        return pixelsSum

"""