import numpy as np
from PIL import Image
import threading
import sys


def resize(data, size):
    imgBuffer = Image.fromarray(data, 'RGB')
    imgBuffer = imgBuffer.resize(size)
    return np.array(imgBuffer)


class Processing(threading.Thread):

    def __init__(self, thisFrame, lastFrame, img, startTime,
                 resizeDivider=32, strengthThreshold=None, countThreshold=None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)

        if countThreshold is None:
            countThreshold = [20, 20, 20]
        if strengthThreshold is None:
            strengthThreshold = [100, 100, 100]

        self.result = None
        self.thisFrame = thisFrame
        self.lastFrame = lastFrame
        self.img = img
        self.startTime = startTime
        self.resizeDivider = resizeDivider
        self.strengthThreshold = strengthThreshold
        self.countThreshold = countThreshold

    def run(self):
        try:
            self.result = self.calculatePosition(self.thisFrame, self.lastFrame)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def calculatePosition(self, thisFrame, lastFrame):
        size = (thisFrame.shape[0], thisFrame.shape[1])
        size = (int(size[1] / self.resizeDivider), int(size[0] / self.resizeDivider))

        thisFrame = resize(thisFrame, size)
        lastFrame = resize(lastFrame, size)

        frameDifference = thisFrame.astype(int) - lastFrame.astype(int)
        pixelsCount = [0, 0, 0]
        pixelsSum = [[0, 0], [0, 0], [0, 0]]
        for y in range(size[1]):
            for x in range(size[0]):
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
                pixelsSum[i] = [int(pixelsSum[i][0] * self.resizeDivider / pixelsCount[i]),
                                int(pixelsSum[i][1] * self.resizeDivider / pixelsCount[i])]

        return pixelsSum
