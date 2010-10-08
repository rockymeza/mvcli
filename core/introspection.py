import inspect
import copy
from collections import namedtuple

def getoptionspec(action):
    """
    (required_options, optional_options, flags, accepts_files, args)
    >>> getoptionspec(lambda x: 1)
    Optionspec(required=['x'], optional=[], flags=[], accepts_files=False, args=['x'])
    >>> getoptionspec(lambda x, y, z = 1: 1)
    Optionspec(required=['x', 'y'], optional=['z'], flags=[], accepts_files=False, args=['x', 'y', 'z'])
    >>> getoptionspec(lambda *x: 1)
    Optionspec(required=[], optional=[], flags=[], accepts_files=True, args=[])
    >>> getoptionspec(lambda x, *y: 1)
    Optionspec(required=['x'], optional=[], flags=[], accepts_files=True, args=['x'])
    >>> getoptionspec(lambda x, y = False: 1)
    Optionspec(required=['x'], optional=[], flags=['y'], accepts_files=False, args=['x', 'y'])
    >>> getoptionspec(lambda foo, bar = 'Hello', verbose = False, debug = False, *files: 1)
    Optionspec(required=['foo'], optional=['bar'], flags=['debug', 'verbose'], accepts_files=True, args=['foo', 'bar', 'verbose', 'debug'])
    >>> getoptionspec(lambda foo = None: 1)
    Optionspec(required=[], optional=['foo'], flags=[], accepts_files=False, args=['foo'])
    >>> class Foo:
    ...     def f(self, x, y = "a.out", z = False):
    ...             pass
    >>> getoptionspec(Foo.f)
    Optionspec(required=['x'], optional=['y'], flags=['z'], accepts_files=False, args=['x', 'y', 'z'])
    """
    argspec = formatargspec(action)
    
    required_options = []
    optional_options = []
    flags = []
    for arg, default in argspec[1].items():
        if isinstance(default, bool):
            flags.append(arg)
        else:
            optional_options.append(arg)

    Optionspec = namedtuple('Optionspec', 'required optional flags accepts_files args')
    return Optionspec(argspec[0], optional_options, flags, argspec[2], argspec[3])

def formatargspec(function):
    """
    (required_options, optional_options, accepts_files args)
    >>> formatargspec(lambda x: 1)
    (['x'], {}, False, ['x'])
    >>> formatargspec(lambda x, y: 1)
    (['x', 'y'], {}, False, ['x', 'y'])
    >>> formatargspec(lambda x = False: 1)
    ([], {'x': False}, False, ['x'])
    >>> formatargspec(lambda x = 'Hello': 1)
    ([], {'x': 'Hello'}, False, ['x'])
    >>> formatargspec(lambda w, x, y = False, z = 'Hello': 1) == (['w', 'x'], {'y': False, 'z': 'Hello'}, False, ['w', 'x', 'y', 'z'])
    True
    >>> formatargspec(lambda *args: 1)
    ([], {}, True, [])
    >>> formatargspec(lambda w, x, y = False, z = 'Hello', *args: 1) == (['w', 'x'], {'y': False, 'z': 'Hello'}, True, ['w', 'x', 'y', 'z'])
    True
    """
    argspec = inspect.getargspec(function)

    optional_options = {}

    # if is method, throw away self argument
    if inspect.ismethod(function):
        argspec.args.pop(0)

    args = copy.copy(argspec.args)
        
    if argspec.defaults:
        defaults = list(argspec.defaults)
        defaults.reverse()
        for value in defaults:
            optional_options[args.pop()] = value

    # accepts files?
    accepts_files = True if argspec.varargs else False

    return (args, optional_options, accepts_files, argspec.args)

import doctest
doctest.testmod()
