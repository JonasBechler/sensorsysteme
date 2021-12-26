import cv2
from abc import ABC, abstractmethod


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
    def evaluate(self, data):
        # data = [[img, calculatedPositionRGB, time], ...]
        pass

    def __str__(self):
        return self.name




class currentFPSandDT(IEvaluationStrategy):
    name = "currentFPSandDT"
    dataPoints = 2

    def evaluate(self, data):
        def currentTimeDiff():
            return data[0][2] - data[1][2]

        def currentFPS():
            return 1 / currentTimeDiff()

        img = data[0][0]
        if data[0][2] in None:
            return img
        debugFps = "fps: " + ('%.3f' % currentFPS())
        debugDt = "dt: " + ('%.3f' % (currentTimeDiff() * 1000))
        cv2.putText(img, debugFps, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        return img


class averageFPSandDT(IEvaluationStrategy):
    name = "averageFPSandDT"
    dataPoints = 30

    def evaluate(self, data):
        def averageFPS():
            fpsSum = 0
            for i in range(self.dataPoints - 1):
                fpsSum = fpsSum + 1 / (data[i][2] - data[i + 1][2])
            fpsSum = fpsSum / (self.dataPoints - 1)
            return fpsSum

        def averageTimeDiff():
            timeSum = 0
            for i in range(self.dataPoints - 1):
                timeSum = timeSum + data[i][2] - data[i + 1][2]
            timeSum = timeSum / (self.dataPoints - 1)
            return timeSum

        img = data[0][0]
        if data[0][2] in None:
            return img

        debugFps = "fpsAv: " + ('%.3f' % averageFPS())
        debugDt = "dtAv: " + ('%.3f' % (averageTimeDiff() * 1000))

        cv2.putText(img, debugFps, (20, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 80), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        return img

class showCurrentPositions(IEvaluationStrategy):
    name = "Current Position"
    dataPoints = 1

    def evaluate(self, data):
        img, positions, time = data[0]
        if positions[0][0] is not None:
            cv2.circle(img, (int(positions[0][0]), int(positions[0][1])), 5, (0, 0, 255), cv2.FILLED)
        if positions[1][0] is not None:
            cv2.circle(img, (int(positions[1][0]), int(positions[1][1])), 5, (0, 255, 0), cv2.FILLED)
        if positions[2][0] is not None:
            cv2.circle(img, (int(positions[2][0]), int(positions[2][1])), 5, (255, 0, 0), cv2.FILLED)
        return img

