#Import the required library
from random import randint

import queue
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from time import time

from UseCases.UseCases import UCnormalUse
from Controllers.CamerController import CV2Controller


class TkinterUI(IUiController, Tk):
    def __init__(self):
        self.label = None
        self.cam = None
        Tk.__init__()

    def init(self):
        while self.outputQueue.empty():
            pass
        img = self.outputQueue.get()
        size = str(img.shape[1]+200) + "x" + str(img.shape[0])

        self.tk.geometry(size)


        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.label = Label(self, image=img)
        self.label.pack()
        # create a Button to handle the update Image event
        button = ttk.Button(Tk, text="Update", command=self.update_img)
        button.pack(pady=15)
        Tk.bind("<Return>", self.update_img)

        Tk.mainloop()

    def mainloop(self, n=0):
        Tk.mainloop()

    def setupInterface(self, size):
        self.picture = Label(self, width=size[0], height=size[1]).pack(side=LEFT)
        self.output = Label(self, width=150, height=int(size[1]/2)).pack(side=RIGHT)
        self.setting = Label(self, width=150, height=int(size[1]/2)).pack(side=RIGHT)



    # Define a Function to update to Image
    def update_img(self):
        if self.outputQueue.empty():
            return None
        img = self.outputQueue.get()
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.label.configure(image=img)
        self.label.image = img


if __name__ == '__main__':
    ui = TkinterUI()
    ui.init()


class QtUI(QtWidgets.QMainWindow, IUiController,):
    flex_widget: FlexPlotWidget

    def __init__(self, *args, **kwargs):
        super(QtUI, self).__init__(*args, **kwargs)


        self.setWindowTitle("Live Plotting Sensor Data")
        self.flex_widget = FlexPlotWidget(time_span=5, interval=10)
        self.setCentralWidget(self.flex_widget)

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.time_init = time()


    def update_plot_data(self):
        self.flex_widget.add_data(x=time() - self.time_init,
                                  thumb=randint(0, 100),
                                  index=randint(0, 100),
                                  middle=randint(0, 100),
                                  ring=randint(0, 100))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = QtUI()
    w.show()
    sys.exit(app.exec_())



