import sys
sys.path.extend(['..', '.'])
from core.introspection import *

class C:
    attribute = True
    def __init__(self): pass
    def foo(self): pass
    def bar(self): pass
    
def test_getactions():
    assert getactions(C) == {'foo': C.foo, 'bar': C.bar}

class Foo:
    def f(self, x, y = 'a.out', z = False):
        pass

def test_optionspec():
    # test for 1 required
    assert getoptionspec(lambda x: 1) == Optionspec(required=['x'], optional=[], flags=[], accepts_files=False)
    # test for 2 required, 1 optional
    assert getoptionspec(lambda x, y, z = 1: 1) == Optionspec(required=['x', 'y'], optional=['z'], flags=[], accepts_files=False)
    # test for accepts_files
    assert getoptionspec(lambda *x: 1) == Optionspec(required=[], optional=[], flags=[], accepts_files=True)
    # test for 1 required, accepts_files
    assert getoptionspec(lambda x, *y: 1) == Optionspec(required=['x'], optional=[], flags=[], accepts_files=True)
    # test for 1 required, 1 flag
    assert getoptionspec(lambda x, y = False: 1) == Optionspec(required=['x'], optional=[], flags=['y'], accepts_files=False)
    # test for 1 required, 1 optional, 2 flags, accepts_files
    assert getoptionspec(lambda foo, bar = 'Hello', verbose = False, debug = False, *files: 1) == Optionspec(required=['foo'], optional=['bar'], flags=['debug', 'verbose'], accepts_files=True)
    # test for 1 optional that defaults to None
    assert getoptionspec(lambda foo = None: 1) == Optionspec(required=[], optional=['foo'], flags=[], accepts_files=False)
    # test for method (strip self option)
    assert getoptionspec(Foo.f) == Optionspec(required=['x'], optional=['y'], flags=['z'], accepts_files=False)

def test_formatargspec():
    assert formatargspec(lambda x: 1) == (['x'], {}, False)
    assert formatargspec(lambda x, y: 1) == (['x', 'y'], {}, False)
    assert formatargspec(lambda x = False: 1) == ([], {'x': False}, False)
    assert formatargspec(lambda x = 'Hello': 1) == ([], {'x': 'Hello'}, False)
    assert formatargspec(lambda w, x, y = False, z = 'Hello': 1) == (['w', 'x'], {'y': False, 'z': 'Hello'}, False)
    assert formatargspec(lambda *args: 1) == ([], {}, True)
    assert formatargspec(lambda w, x, y = False, z = 'Hello', *args: 1) == (['w', 'x'], {'y': False, 'z': 'Hello'}, True)

def test_getmeta():
    def foo():
        pass
    assert getmeta(foo) == {}

    def bar():
        """
        Description: This is bar
        Usage: bar
        """
        pass
    assert getmeta(bar) == {'description': 'This is bar', 'usage': 'bar'}
