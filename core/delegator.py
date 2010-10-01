from core.config import config
from core.request import request
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
        self.route()
        self.delegate()

    def route(self):
        """
        Creates a Request object out of argv
        """
        request['controller'] = config['default_controller']
        request['action'] = config['default_action']
        
        if len(self.argv) > 0:
            request['controller'] = self.argv[0]
            if len(self.argv) > 1:
                request['action'] = self.argv[1]
                if len(self.argv) > 2:
                    request['parameters'] = self.argv[2:]

        return request

    def delegate(self):
        """
        Takes a Request object and instantiates the corresponding controller and
        calls a method based on the action
        """
        if request['controller'] in controllers:
            controller = controllers[request['controller']]()
            try:
                action = getattr(controller, request['action'])
            except:
                print "ActionNotFoundError: That does not exist, better error handling to come soon"
            else:
                action()
        else:
            print "ControllerNotFoundError: That does not exist, better error handling to come soon"

