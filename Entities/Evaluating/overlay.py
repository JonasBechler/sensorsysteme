import cv2
import numpy as np
import pathlib
from PIL import Image

from .base import IEvaluationStrategy
import matplotlib.image as img




class showSilhouette(IEvaluationStrategy):
    name = "Silhouette"
    dataPoints = 1

    # reading png image file
    folderpath = pathlib.Path(__file__).parent.absolute()
    fullpath = folderpath/'Silhouette.png'
    overlay = cv2.imread(str(fullpath), cv2.IMREAD_UNCHANGED)
    pass

    def evaluate(self, img, positions, times):
        background = img
        foreground = self.overlay
        # normalize alpha channels from 0-255 to 0-1
        alpha_foreground = foreground[:, :, 3] / 255.0

        # set adjusted colors
        for color in range(0, 3):
            background[:, :, color] = alpha_foreground * foreground[:, :, color] + \
                                      background[:, :, color] * (1 - alpha_foreground)


        return background


class frameDivider(IEvaluationStrategy):
    name = "frame divider"
    dataPoints = 1

    def __init__(self, frameDivider=32):
        self.frameDivider = frameDivider
        self.name = f"frame divider {frameDivider}"

    def evaluate(self, img, positions, times):
        h, w, _ = img.shape
        img = Image.fromarray(img)
        img = img.resize((int(w / self.frameDivider), int(h / self.frameDivider)))
        img = img.resize((int(w), int(h)), Image.NEAREST)
        img = np.array(img)
        return img