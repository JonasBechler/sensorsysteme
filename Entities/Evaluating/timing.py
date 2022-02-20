import cv2

from .base import IEvaluationStrategy


class currentFPSandDT(IEvaluationStrategy):
    name = "currentFPSandDT"
    dataPoints = 2

    def evaluate(self, img, positions, times):

        def currentTimeDiff():
            return times[0] - times[1]

        def currentFPS():
            return 1 / currentTimeDiff()

        if times[0] is None:
            debugFps = "fps: " + ('%.3f' % 30)
            debugDt = "dt: " + ('%.3f' % (1 / 30 * 1000))
        else:
            debugFps = "fps: " + ('%.3f' % currentFPS())
            debugDt = "dt: " + ('%.3f' % (currentTimeDiff() * 1000))
        cv2.rectangle(img, (0, 0), (250, 45), (255, 255, 255), -1)
        cv2.rectangle(img, (0, 0), (250, 45), (0, 0, 0), 1)
        cv2.putText(img, debugFps, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

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
            debugFps = "fpsAv: " + ('%.3f' % 30)
            debugDt = "dtAv: " + ('%.3f' % (1 / 30 * 1000))
        else:
            debugFps = "fpsAv: " + ('%.3f' % averageFPS())
            debugDt = "dtAv: " + ('%.3f' % (averageTimeDiff() * 1000))

        cv2.rectangle(img, (0, 45), (250, 85), (255, 255, 255), -1)
        cv2.rectangle(img, (0, 45), (250, 85), (0, 0, 0), 1)
        cv2.putText(img, debugFps, (20, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 80), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

        return img
