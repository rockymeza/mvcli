import config
import formatter
import request
import delegator
import exceptions

class MVCLI(object):
    def __init__(self):
        self.config = config.Config()
        self.controllers = ControllerDict()
        self.formatter = formatter.Formatter(self)
        self.views = {}

    @property
    def title(self):
        """
        returns a default title
        """
        return 'App using MVCLI'
        

    def add_controller(self, controller, *routes):
        for route in routes:
            self.controllers[route] = controller

        self.controllers.items()

    def run(self, argv):
        argv = Argv(argv or [])
        self.filename = argv.pop(0)
        self.request = delegator.route(argv, self.config)

        try:
            return delegator.delegate(self)
        except exceptions.ControllerError as e:
            print '%s is not a valid command.' % e
        except exceptions.ActionError as e:
            print '%s is not a valid subcommand.' % e
        except exceptions.OptionError as e:
            print '%s is not a valid option.' % e
        except exceptions.NoFilesError:
            print 'This command does not accept files.'
        except exceptions.MissingOptionError as e:
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

class ControllerDict(dict):
    """
    This is a bad idea, but I like it
    """
    def reverse_items(self):
        reverse_dict = {}
        for alias, controller in self.items():
            if not controller in reverse_dict:
                reverse_dict[controller] = [alias]
            else:
                reverse_dict[controller].append(alias)
                # put the longer alias first
                reverse_dict[controller].sort(lambda x,y: -1 if len(x) >= len(y) else 1)

        return zip(reverse_dict.iterkeys(), reverse_dict.itervalues())


import doctest
doctest.testmod()
