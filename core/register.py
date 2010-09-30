controllers = {}
views = {}

def register_controller(controller, *args):
    """
    Register a controller in the controllers dictionary.
    """
    for alias in args:
        controllers[alias] = controller

