from core.request import request
from core.config import config

controllers = {}
views = {}

def register_controller(controller, *aliases):
    """
    Register a controller in the controllers dictionary.
    """
    for alias in aliases:
        controllers[alias] = controller

def controller(*routes):
    """
    Decorator that registers the controller and gives it some
    useful properties
    """
    def f(controller):
        controller.request = request
        controller.config = config
        register_controller(controller, *routes)
        return controller
    return f
