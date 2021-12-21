import time

from UseCases.TakePictureUC import ICameraController
import cv2

cap = cv2.VideoCapture(0)


class CV2Controller(ICameraController):
    def __init__(self):
        pass

    def takePicture(self):
        t = time.time()
        _, img = cap.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img, t
