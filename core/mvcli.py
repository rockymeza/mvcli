import config
import request
import delegator
from exceptions import *

class MVCLI(object):
    def __init__(self):
        self.config = config.Config()
        self.controllers = {}
        self.views = {}

    def add_controller(self, controller, *routes):
        for route in routes:
            self.controllers[route] = controller

    def run(self, argv):
        argv = Argv(argv or [])
        self.filename = argv.pop(0)
        request = delegator.route(argv, self.config)
        try:
            return delegator.delegate(request, self.controllers, self.config)
        except ControllerError as e:
            print '%s is not a valid command.' % e
        except ActionError as e:
            print '%s is not a valid subcommand.' % e
        except OptionError as e:
            print '%s is not a valid option.' % e
        except MissingOptionError as e:
            print 'The option(s) %s is/are required.' % e

class Argv(list):
    def shiftflag(self):
        """
        >>> Argv(['--foo', 'bar']).shiftflag()
        '--foo'
        >>> Argv(['-f', 'bar']).shiftflag()
        '-f'
        >>> Argv(['foo', '--bar']).shiftflag()
        >>> Argv().shiftflag()
        """
        if len(self) and self[0].startswith('-'):
            return self.pop(0)

    def shiftarg(self):
        """
        >>> Argv(['foo', '--bar']).shiftarg()
        'foo'
        >>> Argv(['--foo', 'bar']).shiftarg()
        >>> Argv().shiftarg()
        """
        if len(self) and not self[0].startswith('-'):
            return self.pop(0)

import doctest
doctest.testmod()
