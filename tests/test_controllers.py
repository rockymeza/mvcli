import sys
sys.path.extend(['..', '.'])
from core.controllers import *

def test_actions():
    """
    Related controllers can not share the same
    actions dictionary.
    """
    class AbstractController(Controller):
        pass
    class Foo(AbstractController):
        pass
    class Bar(AbstractController):
        pass

    AbstractController.action('helper', 1)
    Foo.action('foo action', 2)
    Bar.action('bar action', 3)

    assert 'foo action' not in Bar.actions
    assert 'bar action' not in Foo.actions
    assert Foo.actions['foo action'].description == 2
    assert Bar.actions['bar action'].description == 3
    #assert Foo.actions['helper'].description == 1
    #assert Bar.actions['helper'].description == 1
