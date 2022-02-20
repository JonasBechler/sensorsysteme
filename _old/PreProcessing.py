import sys
import threading
import time

import cv2

from Processing import Processing

cap = cv2.VideoCapture(0)


class PreProcessing(threading.Thread):
    def __init__(self, threadBuffer, targetFps=30,
                 resizeDivider=32, strengthThreshold=None, countThreshold=None,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.threads = threadBuffer
        self.targetDeltaT = 1 / targetFps

        self.resizeDivider = resizeDivider
        self.strengthThreshold = strengthThreshold
        self.countThreshold = countThreshold

    def run(self):
        _, img = cap.read()
        thisFrame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        startTime = time.time()
        currentTime = time.time()

        while True:
            try:
                _, img = cap.read()

                lastFrame = thisFrame
                thisFrame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                if not self.threads.full():
                    thread = Processing(thisFrame, lastFrame, img, currentTime,
                                        resizeDivider=self.resizeDivider, strengthThreshold=self.strengthThreshold,
                                        countThreshold=self.countThreshold)
                    thread.start()
                    self.threads.put(thread)

                while time.time() < startTime:
                    pass
                currentTime = time.time()
                startTime = currentTime + self.targetDeltaT

            except Exception as exc:
                print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception
