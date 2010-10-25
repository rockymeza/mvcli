import nose
import sys
sys.path.extend(['..', '.'])
from core.interface import *

def test_slugify():
    assert slugify('asdf') == 'asdf'
    assert slugify('Foo') == 'foo'
    assert slugify('FooBar') == 'foo-bar'
    assert slugify('BarBazBomb') == 'bar-baz-bomb'

def test_inherits_from_interface():
    class Foo:
        __metaclass__ = InterfaceMeta

    class Bar(Interface):
        __metaclass__ = InterfaceMeta

    assert isinstance(Foo, InterfaceMeta)
    assert isinstance(Foo(), Interface)
    assert isinstance(Bar, InterfaceMeta)
    assert isinstance(Bar(), Interface)


def test_subcommand_detection():
    class Foo:
        __metaclass__ = InterfaceMeta
    class Bar:
        __metaclass__ = InterfaceMeta
        class Baz:
            __metaclass__ = InterfaceMeta
        class Bomb:
            pass

    assert Foo.sub_commands == []
    assert Bar.sub_commands == [Bar.Baz]

def test_add_command_called():
    global add_command_args
    add_command_args = None
    class Foo:
        __metaclass__ = InterfaceMeta
        @classmethod
        def add_command(*args):
            global add_command_args
            add_command_args = args
    assert add_command_args == None
    class Foo:
        __metaclass__ = InterfaceMeta
        @classmethod
        def add_command(*args):
            global add_command_args
            add_command_args = args
        class Bar:
            __metaclass__ = InterfaceMeta
            pass
    assert add_command_args == (Foo, 'Bar', Foo.Bar)

def test_use_parent_called():
    global use_parent_args
    use_parent_args = None
    class Foo:
        __metaclass__ = InterfaceMeta
        @classmethod
        def use_parent(*args):
            global use_parent_args
            use_parent_args = args
    assert use_parent_args == None
    class Foo:
        __metaclass__ = InterfaceMeta
        class Bar:
            __metaclass__ = InterfaceMeta
            @classmethod
            def use_parent(*args):
                global use_parent_args
                use_parent_args = args
            pass
    assert use_parent_args == (Foo.Bar, Foo)


def test_staticmethods():
    # The desirability of this is debatable.
    class Foo:
        __metaclass__ = InterfaceMeta
        def f():
            pass
        @classmethod
        def j(cls):
            assert cls == Foo
    Foo.f() # will fail with an exception if it's not a static method
    Foo.j() # classmethods shouldn't be mangled

def test_default_consume():
    class Foo:
        __metaclass__ = InterfaceMeta
    x = [1, 2]
    Foo.consume(x)
    assert x == [2]

def test_responds_to():
    class Foo:
        __metaclass__ = InterfaceMeta
        name = re.compile('^blah$')
        class Bar:
            __metaclass__ = InterfaceMeta
            pass
    assert Foo.responds_to(['blah'])
    assert Foo.Bar.responds_to(['bar'])

def test_run_simple():
    global bar_action_called
    global action_called
    bar_action_called = False
    action_called = False
    class Foo:
        __metaclass__ = InterfaceMeta
        def action(*args):
            global action_called
            action_called = True
        class Bar:
            __metaclass__ = InterfaceMeta
            def action(*args):
                global bar_action_called
                bar_action_called = args

    Foo.run(['foo'])
    assert action_called
    assert not bar_action_called

    bar_action_called = False
    action_called = False
    Foo.run(['foo', 'bar'])
    assert not action_called
    assert bar_action_called == ()

def test_run_controller():
    global controller_called
    controller_called = False
    class Foo:
        __metaclass__ = InterfaceMeta
        def action():
            pass
        class Sub:
            __metaclass__ = InterfaceMeta
        class controller:
            @classmethod
            def run(*args):
                global controller_called
                controller_called = True
    Foo.run(['foo'])
    assert controller_called == True

@nose.tools.raises(NotImplementedError)
def test_default_action():
    class Foo:
        __metaclass__ = InterfaceMeta
    Foo.run(['foo'])

