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
            


def parse_args(argv):
    """
    Parse a list of GNU or Unix style options, returning a tuple
    of (kwargs, files, options)

    >>> parse_args(['foo'])
    ({}, ['foo'], [])

    >>> parse_args(['-foo'])
    ({}, [], ['foo'])

    >>> parse_args(['--foo'])
    ({}, [], ['foo'])

    >>> parse_args(['-a', 'foo', 'baz', '-b', '--foo=b=ar'])
    ({'a': 'foo', 'foo': 'b=ar'}, ['baz'], ['b'])

    >>> parse_args(['file', '-a', '-b', '-c', 'arg'])
    ({'c': 'arg'}, ['file'], ['a', 'b'])

    """
    # Yay, excuse to use the doctest module.
    # I'm slight dissapointed, it only compares strings, so
    # if you expect {1:'a', 2:'b'}, but get {2:'b', 1:'a'},
    # it fails.

    kwargs = {}
    files = []
    options = []
    #ugly!
    look_behind_key = None

    for arg in argv:
        if arg[0] == '-':
            if look_behind_key:
                # this is an option, and an option can't be the value
                # for an argument
                options.append(look_behind_key)
                look_behind_key = None
            if len(arg) > 1 and arg[1] == '-':
                # gnu-style option
                (key, ignore, value) = arg[2:].partition('=')
                if value:
                    kwargs[key] = value
                else:
                    options.append(key)
            else:
                # a unix-style option. don't do anything now,
                # we don't know if we've got an argument yet
                look_behind_key = arg[1:]
        else:
            # this is not an option, so it's either a unix argument or a file
            if look_behind_key:
                # args is [... -look_behind_key, arg, ...]
                kwargs[look_behind_key] = arg
                look_behind_key = None
            else:
                files.append(arg)
    if look_behind_key:
        options.append(look_behind_key)

    return (kwargs, files, options)
