from abc import ABC, abstractmethod

import numpy as np


class IEvaluationStrategy(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def dataPoints(self):
        pass

    @abstractmethod
    def evaluate(self, img, positions, times):
        pass

    def __str__(self):
        return self.name


def map(value, min1, max1, min2, max2):
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2


def pix2pos(data):
    def transform(yPx, xPx):
        x = xPx * 0.2 - 128  # cm
        y = 144 - yPx * 0.2  # cm
        return x, y

    data_real = list()
    for pixPosition in data:
        r, g, b = pixPosition
        data_real.append((transform(*r), transform(*g), transform(*b)))
    return data_real


def smoothData(data, sliceNumber):
    position = list()
    for i in range(len(data) - sliceNumber + 1):
        positions = np.array(data[i:i + sliceNumber + 1])
        positions = positions.astype(float)
        position.append(np.nanmean(positions, axis=0))
    return position
