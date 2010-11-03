import sys
from py.test import raises
sys.path.extend(['..', '.'])
from core.controllers import *
from core import delegator
from core.exceptions import *

def test_actions():
    """
    Related controllers can not share the same
    actions dictionary.
    """
    class AbstractController(Controller):
        def helper(self):
            pass
    class Foo(AbstractController):
        def foo(self):
            pass
    class Bar(AbstractController):
        def bar(self):
            pass

    with raises(ActionError):
        AbstractController().run(delegator.Argv(['abstract-controller', 'foo'])) # test child non-inheritance

    with raises(ActionError):
        Foo().run(delegator.Argv(['foo', 'bar'])) # test sibling non-inheritance

    Foo().run(delegator.Argv(['foo', 'helper'])) # test inheritance
