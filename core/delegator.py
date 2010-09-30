from core.config import config
from controller import *
from core.register import controllers, views

class Delegator:
    """
    Delegator Class handles all requests and delegates them to the correct
    controllers and views
    """
    def __init__(self, argv):
        self.filename = argv.pop(0)
        self.argv = argv
        request = self.route()
        self.delegate(request)

    def route(self):
        """
        Creates a Request object out of argv
        """
        request = {'controller': config.get('default_controller'), 'action': config.get('default_action')}
        if len(self.argv) > 0:
            request['controller'] = self.argv[0]
            if len(self.argv) > 1:
                request['action'] = self.argv[1]
                if len(self.argv) > 2:
                    request['parameters'] = self.argv[2:]

        return request

    def delegate(self, request):
        """
        Takes a Request object and instantiates the corresponding controller and
        calls a method based on the action
        """
        if controllers[request['controller']]:
            controller = controllers[request['controller']]()
            getattr(controller, request['action'])()
            


