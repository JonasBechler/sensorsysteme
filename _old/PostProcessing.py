import sys

import cv2

from StorageArray import StorageArray


class PostProcessing:
    def __init__(self, threadBuffer, maxCount=50, *args, **kwargs):
        self.threads = threadBuffer
        self.storage = StorageArray(maxCount=maxCount)

    def run(self):
        # fill buffer
        for i in range(self.storage.maxCount):
            while self.threads.empty():
                pass
            thread = self.threads.get()
            thread.join()
            self.storage.push(thread)

        while True:
            try:
                while not self.threads.empty():
                    lastThread = self.threads.get()
                    lastThread.join()
                    img = lastThread.img
                    self.storage.push(lastThread)

                    result = lastThread.result
                    self.show(img)

            except Exception as exc:
                print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def showDebug(self, img, debugText1=None, debugText2=None, debugText3=None):
        def currentFPS():
            return 1 / (self.storage.at(0).startTime - self.storage.at(1).startTime)

        def averageFPS():
            fpsSum = 0
            for i in range(self.storage.maxCount - 1):
                fpsSum = fpsSum + 1 / (self.storage.at(i).startTime - self.storage.at(i + 1).startTime)
            fpsSum = fpsSum / (self.storage.maxCount - 1)
            return fpsSum

        def currentTimeDiff():
            return self.storage.at(0).startTime - self.storage.at(1).startTime

        def averageTimeDiff():
            timeSum = 0
            for i in range(self.storage.maxCount - 1):
                timeSum = timeSum + self.storage.at(i).startTime - self.storage.at(i + 1).startTime
            timeSum = timeSum / (self.storage.maxCount - 1)
            return timeSum

        debugFps = "fpsAv: " + ('%.3f' % averageFPS())
        debugDt = "dtAv: " + ('%.3f' % (averageTimeDiff() * 1000))

        cv2.putText(img, debugFps, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        cv2.putText(img, debugDt, (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        if debugText2 is not None:
            cv2.putText(img, debugText1, (20, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        if debugText2 is not None:
            cv2.putText(img, debugText2, (20, 80), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        if debugText3 is not None:
            cv2.putText(img, debugText2, (20, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

    def showCurrentPositions(self, img):
        result = self.storage.at(0).result
        if result[0][0] is not None:
            cv2.circle(img, (int(result[0][0]), int(result[0][1])), 5, (0, 0, 255), cv2.FILLED)
        if result[1][0] is not None:
            cv2.circle(img, (int(result[1][0]), int(result[1][1])), 5, (0, 255, 0), cv2.FILLED)
        if result[2][0] is not None:
            cv2.circle(img, (int(result[2][0]), int(result[2][1])), 5, (255, 0, 0), cv2.FILLED)

    def showPath(self, img, pathLen):
        def calculatePaths(pathLen):
            paths = [((None, None),
                      (None, None),
                      (None, None))] * pathLen

            for c in range(3):
                pass

            return paths

        if pathLen >= self.storage.maxCount:
            pass
        else:
            paths = calculatePaths(pathLen)
            if paths[0][0] is not None:
                for i in range(pathLen):
                    pass
                    # cv2.line(img, path.start_point, path.end_point, color, thickness)

    def show(self, img):
        self.showDebug(img)
        self.showCurrentPositions(img)
        self.showPath(img, 5)

        cv2.imshow("Juggling Tracking", img)
        cv2.waitKey(1)
