# Sensorsysteme
import sys

from PyQt5 import QtWidgets

from Controllers.Gui.Controller import Controller

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pyqtController = Controller()
    sys.exit(app.exec_())
