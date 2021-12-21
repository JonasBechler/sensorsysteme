# Sensorsysteme
import sys

from PyQt5.QtWidgets import QApplication
from Controllers.Gui import PyQtController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pyqtController = PyQtController()
    sys.exit(app.exec_())
