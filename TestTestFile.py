import os
import pickle

import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui


class FileLoader:
    def testNames(self):
        testFolderPath = "/Users/jonas/Workspaces/Pycharm/Sensorsysteme/TestFiles"
        testFileNames = os.listdir(testFolderPath)
        return testFileNames

    def loadTests(self, testName):
        testFolderPath = "/Users/jonas/Workspaces/Pycharm/Sensorsysteme/TestFiles"
        with open(testFolderPath + "/" + testName, "rb") as f:
            return pickle.load(f)
        return


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.fileLoader = FileLoader()
        testNames = self.fileLoader.testNames()
        self.data = self.fileLoader.loadTests(testNames[0])

        self.picture = QtWidgets.QLabel()
        self.setCentralWidget(self.picture)
        self.setPicture()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Right:
            self.index = self.index + 1
            if self.index >= len(self.data):
                self.index = len(self.data) - 1
            self.setPicture()
        if e.key() == QtCore.Qt.Key_Left:
            self.index = self.index - 1
            if self.index < 0:
                self.index = 0

    def setPicture(self):
        currentPic = np.array(self.data[self.index]).astype(int)
        lastPic = np.array(self.data[self.index + 1]).astype(int)
        diffPic = cv2.absdiff(currentPic, lastPic, )

        img = diffPic
        img.astype(np.uint8)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        image = QtGui.QImage(img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        image = QtGui.QPixmap.fromImage(image)
        self.picture.setPixmap(image)


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


def main(index=0, data=None):
    def frameDif(frame, dif):
        h, w, _ = frame.shape
        img = Image.fromarray(frame)
        img = img.resize((int(w / dif), int(h / dif)))
        # img = img.resize((int(w), int(h)), Image.NEAREST)
        img = np.array(img)
        return img

    def frameUp(template, frame):
        h, w, _ = template.shape
        img = Image.fromarray(frame)
        # img = img.resize((int(w * up), int(h * up)))
        img = img.resize((int(w), int(h)), Image.NEAREST)
        img = np.array(img)
        return img

    def onlyColor(frame_rgb):
        frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
        color_mask = cv2.inRange(frame_hsv, dark_color, light_color)
        return cv2.bitwise_and(frame_rgb, frame_rgb, mask=color_mask)

    frameDivider = 8
    currentPic = np.array(data[index])
    currentPic_rgb = frameDif(currentPic, frameDivider)
    currentPic_rgb_oC = onlyColor(currentPic_rgb)

    lastPic = np.array(data[index + 1])
    lastPic_rgb = frameDif(lastPic, frameDivider)
    lastPic_rgb_oC = onlyColor(lastPic_rgb)

    absDiff = np.absolute(currentPic_rgb_oC.astype(float) - lastPic_rgb_oC.astype(float))
    absDiff = absDiff.astype(np.uint8)
    # cv2.imshow("img", absDiff)

    hsvDiff = cv2.cvtColor(absDiff, cv2.COLOR_RGB2HSV)
    cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/diff_hsv_0.png', hsvDiff)

    green_mask = cv2.inRange(hsvDiff, dark_green, light_green)
    indexes_green = np.where((green_mask == 255))
    res_green = (None, None)
    if len(indexes_green[0]) > 1:
        res_green = np.mean(indexes_green, axis=1)
        cv2.circle(hsvDiff, (int(res_green[1]), int(res_green[0])), 10, (255, 255, 255), cv2.FILLED)
        res_green = res_green * frameDivider
        cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/diff_hsv_1.png', hsvDiff)

    red_mask1 = cv2.inRange(hsvDiff, dark_red, right_red)
    red_mask2 = cv2.inRange(hsvDiff, left_red, light_red)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    indexes_red = np.where((red_mask == 255))
    res_red = (None, None)
    if len(indexes_red[0]) > 1:
        res_red = np.mean(indexes_red, axis=1)
        cv2.circle(hsvDiff, (int(res_red[1]), int(res_red[0])), 10, (255, 255, 255), cv2.FILLED)
        res_red = res_red * frameDivider
        cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/diff_hsv_2.png', hsvDiff)

    blue_mask = cv2.inRange(hsvDiff, dark_blue, light_blue)
    indexes_blue = np.where((blue_mask == 255))
    res_blue = (None, None)
    if len(indexes_blue[0]) > 1:
        res_blue = np.mean(indexes_blue, axis=1)
        cv2.circle(hsvDiff, (int(res_blue[1]), int(res_blue[0])), 10, (255, 255, 255), cv2.FILLED)
        res_blue = res_blue * frameDivider
        cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/diff_hsv_3.png', hsvDiff)

    hsvDiff = cv2.cvtColor(hsvDiff, cv2.COLOR_HSV2RGB)
    absDiff = frameUp(currentPic, hsvDiff)

    out = cv2.cvtColor(absDiff, cv2.COLOR_RGB2BGR)
    cv2.imshow("img", out)

    cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/input.png', currentPic)
    cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/input_scaled.png', currentPic_rgb)
    cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/input_scaled_oC.png', currentPic_rgb_oC)

    cv2.imwrite('/Users/jonas/Workspaces/Pycharm/Sensorsysteme/Pictures/diff_rgb.png', absDiff)


if __name__ == "__main__":
    index = 0
    fileLoader = FileLoader()
    testNames = fileLoader.testNames()
    data = fileLoader.loadTests("lukas2.pckl")
    pass
    while True:
        main(index=index, data=data)
        cv2.waitKey()

        index = index + 1
