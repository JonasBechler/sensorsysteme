import numpy as np
import cv2

from .base import IProcessingStrategy

S_max = 255
V_max = 255

dark_color = (0, 20, 160)
light_color = (179, 255, 255)

dark_red = (165, 120, 180)
right_red = (179, S_max, V_max)
left_red = (0, 120, 180)
light_red = (20, S_max, V_max)

dark_green = (38, 70, 160)
light_green = (80, S_max, V_max)

dark_blue = (90, 50, 170)
light_blue = (150, S_max, V_max)


class FinalStrategy(IProcessingStrategy):
    name = "final"

    frameDivider = 16
    frameCount = 2

    def __init__(self, name, frameDivider=32, borders=None):

        self.name = f"{name} {frameDivider}"
        self.frameDivider = frameDivider

    def calculate(self, frames) -> [[float, float], [float, float], [float, float]]:
        def onlyColor(frame_rgb):
            frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
            color_mask = cv2.inRange(frame_hsv, dark_color, light_color)
            return cv2.bitwise_and(frame_rgb, frame_rgb, mask=color_mask)

        currentPic = np.array(frames[0])
        currentPic_rgb_oC = onlyColor(currentPic)
        lastPic = np.array(frames[1])
        lastPic_rgb_oC = onlyColor(lastPic)

        absDiff = np.abs(currentPic_rgb_oC.astype(float) - lastPic_rgb_oC.astype(float))
        absDiff = absDiff.astype(np.uint8)

        hsvDiff = cv2.cvtColor(absDiff, cv2.COLOR_RGB2HSV)

        green_mask = cv2.inRange(hsvDiff, dark_green, light_green)
        indexes_green = np.where((green_mask == 255))
        res_green = (None, None)
        if len(indexes_green[0]) > 1:
            res_green = np.mean(indexes_green, axis=1)
            cv2.circle(hsvDiff, (int(res_green[1]), int(res_green[0])), 10, (255, 255, 0), cv2.FILLED)
            res_green = res_green * self.frameDivider

        red_mask1 = cv2.inRange(hsvDiff, dark_red, right_red)
        red_mask2 = cv2.inRange(hsvDiff, left_red, light_red)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        indexes_red = np.where((red_mask == 255))
        res_red = (None, None)
        if len(indexes_red[0]) > 1:
            res_red = np.mean(indexes_red, axis=1)
            cv2.circle(hsvDiff, (int(res_red[1]), int(res_red[0])), 10, (255, 255, 0), cv2.FILLED)
            res_red = res_red * self.frameDivider

        blue_mask = cv2.inRange(hsvDiff, dark_blue, light_blue)
        indexes_blue = np.where((blue_mask == 255))
        res_blue = (None, None)
        if len(indexes_blue[0]) > 1:
            res_blue = np.mean(indexes_blue, axis=1)
            res_blue = res_blue * self.frameDivider

        return res_red, res_green, res_blue
