import inspect
import copy

def getoptionspec(action):
    """
    (optional_keywords, required_keywords, booleans, minfiles, maxfiles)

    >>> getoptionspec(lambda x: 1)
    ([], [], [], 1, 1)
    >>> getoptionspec(lambda x, y, z = 1: 1)
    ([], [], [], 2, 3)
    >>> getoptionspec(lambda *x: 1)
    ([], [], [], 0, -1)
    >>> getoptionspec(lambda x, *y: 1)
    ([], [], [], 1, -1)
    >>> getoptionspec(lambda y, x = False: 1)
    ([], [], ['x'], 1, 1)
    >>> getoptionspec(lambda *, y = "a.out": 1)
    (['y'], [], [], 0, 0)
    >>> getoptionspec(lambda x = False, *, y: 1)
    ([], ['y'], ['x'], 0, 0)
    >>> getoptionspec(lambda x = "hello", z = False, *, y: 1)
    ([], ['y'], ['z'], 0, 1)
    >>> getoptionspec(lambda x, y, z = False, *, foo = 1, bar: 1)
    (['foo'], ['bar'], ['z'], 2, 2)
    >>> getoptionspec(lambda x, *files, foo = 1, bar = False:1) #is this the correct behavior?
    (['foo'], [], ['bar'], 1, -1)
    >>> getoptionspec(lambda verbose = False, debug = False, *input_files, output = "a.out":1)
    (['output'], [], ['debug', 'verbose'], 0, -1)
    >>> getoptionspec(lambda **kwargs:1)
    (-1, [], [], 0, 0)
    >>> getoptionspec(lambda x, *, y, **kwargs:1)
    (-1, ['y'], [], 1, 1)
    """

    # inspect gives us an argspec with None instead of an empty list -- very annoying!
    argspec = inspect.FullArgSpec(*[i or {} for i in inspect.getfullargspec(action)])

    default_dict = {}
    args = copy.copy(argspec.args)
    defaults = list(argspec.defaults)
    defaults.reverse()
    for value in defaults:
        default_dict[args.pop()] = value

    booleans = []
    for key in default_dict:
        if isinstance(default_dict[key], bool):
            booleans.append(key)

    optional_keywords = []
    required_keywords = []
    for key in argspec.kwonlyargs:
        if key in argspec.kwonlydefaults and isinstance(argspec.kwonlydefaults[key], bool):
            booleans.append(key)
        elif key in argspec.kwonlydefaults:
            optional_keywords.append(key)
        else:
            required_keywords.append(key)
    if argspec.varkw:
        optional_keywords = -1

    if argspec.varargs:
        maxfiles = -1
    else:
        maxfiles =  len([i for i in argspec.args if i not in booleans])
    minfiles = action.__code__.co_argcount - len(argspec.defaults)

    return (optional_keywords, required_keywords, booleans, minfiles, maxfiles)


import doctest
doctest.testmod()
