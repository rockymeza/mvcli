from request import Request
import exceptions
from introspection import getoptionspec
import collections
import copy

def route(argv, config):
    """
    Creates a Request object out of argv
    """
    request = Request()
    request['controller'] = argv.shiftarg() or config['default_controller']
    request['action'] = argv.shiftarg() or config['default_action']
    request['parameters'] = argv

    return request

def delegate(mvcli):
    """
    Takes a Request object and instantiates the corresponding controller and
    calls a method based on the action
    """
    request = mvcli.request
    config = mvcli.config
    controllers = mvcli.controllers
    if request['controller'] in controllers:
        controller = controllers[request['controller']](mvcli)
        if request['action'] in controller.actions:
            action = getattr(controller, request['action'])
            optionspec = getoptionspec(action)
            arguments = parse_options(optionspec, request['parameters'])

            action(*arguments.args, **arguments.kwargs)
        else:
            raise exceptions.ActionError(request['action'])
    else:
        raise exceptions.ControllerError(request['controller'])

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


Arguments = collections.namedtuple('Arguments', 'args kwargs')
def parse_options(optionspec, argv):
    """
    Arguments(args, kwargs)
    """
    args = {}
    kwargs = {}
    files = []

    required_options = copy.copy(optionspec.required)

    def assignkey(key, value = None):
        # required
        if key in optionspec.required:
            args[key] = value or argv.shiftarg()
            required_options.remove(key)
            if not args[key]:
                raise exceptions.OptionValueError(key)
        # optional
        elif key in optionspec.optional:
            kwargs[key] = value or argv.shiftarg()
            if not kwargs[key]:
                raise exceptions.OptionValueError(key)
        elif key in optionspec.flags:
            kwargs[key] = True
        else:
            raise exceptions.OptionError(key)

    while argv:
        arg = argv.shiftflag()
        if arg:
            if arg.startswith('--'):
                (key, ignore, value) = arg[2:].partition('=')
                assignkey(key, value)
            elif arg.startswith('-'):
                for letter in arg[1:]:
                    assignkey(letter)
        elif optionspec.accepts_files:
            files.append(argv.shiftarg())
        else:
            raise exceptions.NoFilesError(argv.shiftarg())


    # did they forget a required one?
    if required_options:
        raise exceptions.MissingOptionError(required_options)

    arguments = []
    # put them in the right order
    for arg in optionspec.required:
        arguments.append(args[arg])
    
    # add files
    arguments.extend(files)
    return Arguments(arguments, kwargs)


class Argv(list):
    def shiftflag(self):
        if self[0].startswith('-'):
            return self.pop(0)

    def shiftarg(self):
        if not self[0].startswith('-'):
            return self.pop(0)
