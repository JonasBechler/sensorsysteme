# __init__.py
import PyQt5
from .Model import Model
from .View import View
from .Controller import Controller

def start():
    model = Model()
    view = View()
    controller = Controller()