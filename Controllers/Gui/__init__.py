# __init__.py
from .Controller import Controller
from .Model import Model
from .View import View


def start():
    model = Model()
    view = View()
    controller = Controller()
