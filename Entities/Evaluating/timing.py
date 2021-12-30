from .base import IEvaluationStrategy
import cv2


class currentFPSandDT(IEvaluationStrategy):
    name = "currentFPSandDT"
    dataPoints = 2

    def evaluate(self, img, positions, times):

        def currentTimeDiff():
            return times[0] - times[1]

        def currentFPS():
            return 1 / currentTimeDiff()

        if times[0] is None:
            return img
        debugFps = "fps: " + ('%.3f' % currentFPS())
        debugDt = "dt: " + ('%.3f' % (currentTimeDiff() * 1000))
        cv2.putText(img, debugFps, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        return img


class averageFPSandDT(IEvaluationStrategy):
    name = "averageFPSandDT"
    dataPoints = 30

    def evaluate(self, img, positions, times):
        def averageFPS():
            fpsSum = 0
            for i in range(self.dataPoints - 1):
                fpsSum = fpsSum + 1 / (times[i] - times[i + 1])
            fpsSum = fpsSum / (self.dataPoints - 1)
            return fpsSum

        def averageTimeDiff():
            timeSum = 0
            for i in range(self.dataPoints - 1):
                timeSum = timeSum + times[i] - times[i + 1]
            timeSum = timeSum / (self.dataPoints - 1)
            return timeSum

        if times[0] is None:
            return img

        debugFps = "fpsAv: " + ('%.3f' % averageFPS())
        debugDt = "dtAv: " + ('%.3f' % (averageTimeDiff() * 1000))

        cv2.putText(img, debugFps, (20, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 80), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        return img
