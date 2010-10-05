import config
import request
import delegator

class MVCLI(object):
    def __init__(self):
        self.config = config.Config()
        self.controllers = {}
        self.views = {}

    def add_controller(self, *controllers):
        for controller in controllers:
            for route in controller.responds_to:
                self.controllers[route] = controller

    def run(self, argv):
        self.filename = argv.pop(0)
        request = delegator.route(argv, self.config)
        return delegator.delegate(request, self.controllers, self.config)
