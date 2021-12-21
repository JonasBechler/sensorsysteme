import threading
import time
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication


def function(*args, **kwargs):
    for i, arg in enumerate(args):
        print(arg)

    for kw in kwargs:
        if kw == "i":
            print(kwargs[kw])
        if kw == "time":
            print(kwargs[kw])
        if kw == "pos":
            print(kw)
            print(kwargs[kw][0:2])
    print("Hallllllo")

def calc():
    z_real_soll = 4  # mm
    z_real_ist = 3.5  # mm

    steps_ist = 800
    steps_soll = z_real_soll / z_real_ist * steps_ist
    print(steps_soll)


if __name__ == '__main__':
    function()
    pass
    pass
    pass
    calc()

    function("hallo", "was", "geht", i=5, pos=[4, 3, 2])



class Obj (QObject):
    def __init__(self, *args, **kwargs):
        QObject.__init__(self)
        self.t = Thread()
        self.t.start()
        pass


class Thread(QThread):
    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.collectProcessData)

    def collectProcessData(self):
        print ("Collecting Process Data")

    def run(self):
        self.timer.start(1000)
        loop = QEventLoop()
        loop.exec_()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     o = Obj()
#     sys.exit(app.exec_())
