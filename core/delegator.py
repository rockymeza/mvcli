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

def parse_args(argv, takes_args = []): 
    """
    Parse a list of GNU or Unix style options, returning a tuple of
    (kwargs, files, options). takes_args is an iterable of strings
    or compiled regular expressions -- if an option is in here,
    it will consume an argument, otherwise it is treated as a boolean flag.

    >>> parse_args(['foo'])
    ({}, ['foo'], [])

    >>> parse_args(['--foo'])
    ({}, [], ['foo'])

    >>> parse_args(['-a', 'foo', 'baz', '-b', '--foo=b=ar'], 'a')
    ({'a': 'foo', 'foo': 'b=ar'}, ['baz'], ['b'])

    >>> parse_args(['file', '-a', '-b', '-c', 'arg'])
    ({}, ['file', 'arg'], ['a', 'b', 'c'])

    >>> parse_args(['-xzf', 'foo'])
    ({}, ['foo'], ['x', 'z', 'f'])

    >>> parse_args(['-xzf', 'foo'], ['f'])
    ({'f': 'foo'}, [], ['x', 'z'])

    >>> parse_args(['-xzf', 'foo', 'bar'], 'xf')
    ({'x': 'foo', 'f': 'bar'}, [], ['z'])
    
    >>> parse_args(['--foo', 'bar'], ['foo'])
    ({'foo': 'bar'}, [], [])

    >>> parse_args(['--foo', 'bar'])
    ({}, ['bar'], ['foo'])

    """

    kwargs = {}
    files = []
    options = []

    takes_args = MatcherList(takes_args)

    while argv:
        arg = argv.pop(0)
        if arg.startswith('--'):
            # gnu-style option
            (key, ignore, value) = arg[2:].partition('=')
            if value or (key in takes_args):
                kwargs[key] = value or argv.pop(0)
            else:
                options.append(key)
        elif arg.startswith('-'):
            # unix-style option
            for letter in arg[1:]:
                if letter in takes_args:
                    kwargs[letter] = argv.pop(0)
                else:
                    options.append(letter)
        else:
            files.append(arg)
    return (kwargs, files, options)

# rocky's attempt
import re
def parse_flags(argv):
    options = {}
    flags = []
    args = []

    while len(argv) > 0:
        arg = argv.pop(0)
        match = re.match('^--([a-z0-9_]+)(?:=(.*?))?$', arg) or re.match('^-([a-z0-9])(?:=(.*?))?$', arg)
        if match:
            if len(match.groups()) == 2 and match.group(2):
                options[match.group(1)] = match.group(2)
            else: 
                flags.append(match.group(1))
        else:
            args.append(arg)
    
    return (options, flags, args)

class MatcherList(list):
    """
    A list of patterns. Use 'in' to match.

    >>> x = MatcherList(['a', 'b'])
    >>> 'a' in x
    True
    >>> 'c' in x
    False
    >>> 'a' in MatcherList()
    False
    >>> import re
    >>> x = MatcherList(['d', re.compile('a|b')])
    >>> 'a' in x
    True
    >>> 'c' in x
    False
    >>> 'd' in x
    True
    """

    def __contains__(self, item):
        for i in self:
            try:
                if item == i or i.match(item):
                    return True
            except AttributeError:
                pass
        return False
