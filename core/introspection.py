import inspect
import copy
from collections import namedtuple
import re

def getactions(controller):
    """
    >>> class C:
    ...     attribute = True
    ...     def __init__(self): pass
    ...     def foo(self): pass
    >>> getactions(C)
    [('foo', <unbound method C.foo>)]
    """
    actions = []
    members = inspect.getmembers(controller)
    for name, member in members:
        if inspect.ismethod(member) and not name.startswith('__'):
            actions.append((name, member))
    return actions

def getoptionspec(action):
    """
    (required_options, optional_options, flags, accepts_files)
    >>> getoptionspec(lambda x: 1)
    Optionspec(required=['x'], optional=[], flags=[], accepts_files=False)
    >>> getoptionspec(lambda x, y, z = 1: 1)
    Optionspec(required=['x', 'y'], optional=['z'], flags=[], accepts_files=False)
    >>> getoptionspec(lambda *x: 1)
    Optionspec(required=[], optional=[], flags=[], accepts_files=True)
    >>> getoptionspec(lambda x, *y: 1)
    Optionspec(required=['x'], optional=[], flags=[], accepts_files=True)
    >>> getoptionspec(lambda x, y = False: 1)
    Optionspec(required=['x'], optional=[], flags=['y'], accepts_files=False)
    >>> getoptionspec(lambda foo, bar = 'Hello', verbose = False, debug = False, *files: 1)
    Optionspec(required=['foo'], optional=['bar'], flags=['debug', 'verbose'], accepts_files=True)
    >>> getoptionspec(lambda foo = None: 1)
    Optionspec(required=[], optional=['foo'], flags=[], accepts_files=False)
    >>> class Foo:
    ...     def f(self, x, y = "a.out", z = False):
    ...             pass
    >>> getoptionspec(Foo.f)
    Optionspec(required=['x'], optional=['y'], flags=['z'], accepts_files=False)
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

    Optionspec = namedtuple('Optionspec', 'required optional flags accepts_files')
    return Optionspec(argspec[0], optional_options, flags, argspec[2])

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

    # if is method, throw away self argument
    if inspect.ismethod(function):
        argspec.args.pop(0)

    optional_options = {}
    args = copy.copy(argspec.args)
        
    if argspec.defaults:
        defaults = list(argspec.defaults)
        defaults.reverse()
        for value in defaults:
            optional_options[args.pop()] = value

    # accepts files?
    accepts_files = True if argspec.varargs else False

    return (args, optional_options, accepts_files)

def getmeta(function):
    """
    {'description': ..., 'usage': ...}
    >>> def foo():
    ...     pass
    >>> getmeta(foo)
    {}
    >>> def bar():
    ...     "\
    ...     Description: This is bar\
    ...     Usage: bar()\
    ...     "
    >>> getmeta(bar) == {'description': 'This is bar', 'usage': 'bar()'}
    True
    """
    meta = {}
    
    if function.__doc__:
        for key in ['description', 'usage']:
            match = re.search('^' + key +': (.*?)$', function.__doc__)
            if match:
                meta[key] = match.group(0)
    
    return meta


import doctest
doctest.testmod()
