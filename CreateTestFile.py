import pickle
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from Controllers.CamerController import CV2Controller
cam = CV2Controller()


class CreateTestFile(QtWidgets.QWidget):
    i = 0
    data = list()
    dataLen = 100

    def __init__(self):
        super().__init__()
        folderPath = "TestFiles/"
        print("input filename or press x")
        name = input()
        _ = cam.takePicture()
        _ = cam.takePicture()
        print("5")
        time.sleep(1)
        print("4")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("start")

        self.delayTime = int(1000/30)

        if name != "x":
            self.path = folderPath + name + ".pckl"
            self.timer = QTimer()
            self.startTime = time.time()
            self.stopTime = None
            self.timer.setInterval(self.delayTime)
            self.timer.timeout.connect(self.takePicture)
            self.timer.start()

    def takePicture(self):
        pic, _ = cam.takePicture()
        self.data.append(pic)

        if self.i == self.dataLen-1:
            self.stopTime = time.time()
            self.timer.stop()
            fps = self.dataLen / (self.stopTime - self.startTime)
            print("fps was" + str(fps))
            self.saveFile()

        self.i = self.i + 1

    def saveFile(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.data, f)
            f.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    creator = CreateTestFile()
    sys.exit(app.exec_())
