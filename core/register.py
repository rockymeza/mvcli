def register_controller(controller, *aliases):
    """
    Register a controller in the controllers dictionary.
    """
    controller.responds_to = aliases

def controller(*routes):
    """
    Decorator that registers the controller.
    """
    def f(controller):
        register_controller(controller, *routes)
        return controller
    return f
