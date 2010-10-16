import inspect
import copy
from collections import namedtuple
import re

def getactions(controller):
    """
    {'method_name': <method>}
    """
    actions = {}
    members = inspect.getmembers(controller)
    for name, member in members:
        if inspect.ismethod(member) and not name.startswith('__'):
            actions[name] = member
    return actions

Optionspec = namedtuple('Optionspec', 'required optional flags accepts_files')
def getoptionspec(action):
    """
    Optionspec(required_options, optional_options, flags, accepts_files)
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

    return Optionspec(argspec[0], optional_options, flags, argspec[2])

def formatargspec(function):
    """
    (required_options, optional_options, accepts_files)
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
    """
    meta = {}
    
    if function.__doc__:
        for key in ['description', 'usage']:
            match = re.search('^\s*' + key +':\s*(.*?)\s*$', function.__doc__, flags=re.I | re.M)
            if match:
                meta[key] = match.group(1)
    
    return meta
