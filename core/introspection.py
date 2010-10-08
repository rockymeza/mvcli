import inspect
import copy

def getoptionspec(action):
    """
    (required_options, optional_options, flags, accepts_files)
    >>> getoptionspec(lambda x: 1)
    (['x'], [], [], False)
    >>> getoptionspec(lambda x, y, z = 1: 1)
    (['x', 'y'], ['z'], [], False)
    >>> getoptionspec(lambda *x: 1)
    ([], [], [], True)
    >>> getoptionspec(lambda x, *y: 1)
    (['x'], [], [], True)
    >>> getoptionspec(lambda x, y = False: 1)
    (['x'], [], ['y'], False)
    >>> getoptionspec(lambda foo, bar = 'Hello', verbose = False, debug = False, *files: 1)
    (['foo'], ['bar'], ['debug', 'verbose'], True)
    >>> getoptionspec(lambda foo = None: 1)
    ([], ['foo'], [], False)
    >>> class Foo:
    ...     def f(self, x, y = "a.out", z = False):
    ...             pass
    >>> getoptionspec(Foo.f)
    (['x'], ['y'], ['z'], False)
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

    return (argspec[0], optional_options, flags, argspec[2])

def formatargspec(function):
    """
    (required_options, optional_options, accepts_files)
    >>> formatargspec(lambda x: 1)
    (['x'], {}, False)
    >>> formatargspec(lambda x, y: 1)
    (['x', 'y'], {}, False)
    >>> formatargspec(lambda x = False: 1)
    ([], {'x': False}, False)
    >>> formatargspec(lambda x = 'Hello': 1)
    ([], {'x': 'Hello'}, False)
    >>> formatargspec(lambda w, x, y = False, z = 'Hello': 1) == (['w', 'x'], {'y': False, 'z': 'Hello'}, False)
    True
    >>> formatargspec(lambda *args: 1)
    ([], {}, True)
    >>> formatargspec(lambda w, x, y = False, z = 'Hello', *args: 1) == (['w', 'x'], {'y': False, 'z': 'Hello'}, True)
    True
    """
    argspec = inspect.getargspec(function)

    optional_options = {}
    args = copy.copy(argspec.args)

    # if is method, throw away self argument
    if inspect.ismethod(function):
        args.pop(0)
        
    if argspec.defaults:
        defaults = list(argspec.defaults)
        defaults.reverse()
        for value in defaults:
            optional_options[args.pop()] = value

    # accepts files?
    accepts_files = True if argspec.varargs else False

    return (args, optional_options, accepts_files)

import doctest
doctest.testmod()
