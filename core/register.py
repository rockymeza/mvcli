controllers = {}
views = {}

def register_controller(controller, *args):
    """
    Register a controller in the controllers dictionary.
    """
    for alias in args:
        controllers[alias] = controller

def route(*routes):
    """
    Pretty decorator wrapper for register_controller
    """
    def f(controller):
        register_controller(controller, *routes)
        return controller
    return f
