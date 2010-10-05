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
    Decorator that registers the controller.
    """
    def f(controller):
        register_controller(controller, *routes)
        return controller
    return f
