import nose
import sys
sys.path.extend(['..', '.'])
from core.interface import *
from core import delegator

def test_inherits_from_interface():
    class Foo:
        __metaclass__ = InterfaceMeta

    class Bar(Interface):
        __metaclass__ = InterfaceMeta

    class Baz(Interface):
        pass

    assert isinstance(Foo, InterfaceMeta)
    assert isinstance(Foo(), Interface)
    assert isinstance(Bar, InterfaceMeta)
    assert isinstance(Bar(), Interface)
    assert isinstance(Baz, InterfaceMeta) # Inheriting from Interface sets the metaclass
    assert isinstance(Baz(), Interface)


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

def test_interface_instantiated():
    global init_args
    init_args = None
    class Foo(Interface):
        def __init__(*args):
            global init_args
            init_args = args
    assert init_args == None
    class Bar(Interface):
        foo = Foo
    assert type(init_args[0]) == Foo
    assert init_args[1:] == ('foo', Bar)

def test_default_consume():
    class Foo:
        __metaclass__ = InterfaceMeta
    x = [1, 2]
    Foo().consume(x)
    assert x == [2]

def test_responds_to():
    class Foo:
        __metaclass__ = InterfaceMeta
        name = 'blah'
        class Bar:
            __metaclass__ = InterfaceMeta
            pass
    assert Foo.Bar.responds_to(['bar'])
    assert Foo().Bar.responds_to(['bar'])

def test_run_simple():
    global bar_action_called
    global action_called
    bar_action_called = False
    action_called = False
    class Foo:
        __metaclass__ = InterfaceMeta
        def action(self, *args):
            global action_called
            action_called = True
        class Bar:
            __metaclass__ = InterfaceMeta
            def action(self, *args):
                global bar_action_called
                bar_action_called = args

    Foo().run(delegator.Argv(['foo']))
    assert action_called
    assert not bar_action_called

    bar_action_called = False
    action_called = False
    Foo().run(delegator.Argv(['foo', 'bar']))
    assert not action_called
    assert bar_action_called == ()

def test_run_controller():
    global controller_called
    controller_called = False
    class Controller(Interface):
        def run(*args):
            global controller_called
            controller_called = True
    class Foo(Controller):
        __metaclass__ = InterfaceMeta
        def action():
            pass
    Foo().run(delegator.Argv(['foo']))
    assert controller_called == True

@nose.tools.raises(NotImplementedError)
def test_default_action():
    class Foo:
        __metaclass__ = InterfaceMeta
    Foo().run(delegator.Argv(['foo']))

def test_doesnt_share():
    class Foo(Interface):
        class a(Interface):
            pass
    class Bar(Interface):
        class b(Interface):
            pass

    assert Bar.sub_commands != Foo.sub_commands

def test_inheritance():
    global parent_foo_called
    class Parent(Interface):
        class Foo(Interface):
            @staticmethod
            def action():
                global parent_foo_called
                parent_foo_called = True
    class Foo(Parent):
        class A(Interface):
            pass
    class Bar(Parent):
        class B(Interface):
            pass

    Foo().run(delegator.Argv(['foo', 'foo']))
    assert parent_foo_called == True
    assert Foo.A in Foo.sub_commands
    assert Bar.B not in Foo.sub_commands

    parent_foo_called = False
    Bar().run(delegator.Argv(['bar', 'foo']))
    assert parent_foo_called == True
    assert Bar.B in Bar.sub_commands
    assert Foo.A not in Bar.sub_commands

def test_help_does_something():
    class Foo(Interface):
        help = BuiltinHelp
        description = 'bar'
        class Bar(Interface):
            description = 'foo'
            class Baz(Interface):
                description = 'bomb'
    Foo().run(delegator.Argv(['foo', 'help']))
    Foo().run(delegator.Argv(['foo', 'help', 'bar']))
    Foo().run(delegator.Argv(['foo', 'bar', 'help', 'baz']))
    @nose.tools.raises(Exception)
    def f():
        Foo.run(delegator.Argv(['foo', 'baz', 'help']))
    f()

def test_rename():
    global bar_action_called
    bar_action_called = False
    class Foo(Interface):
        class Bar(Interface):
            def action(self, *args):
                global bar_action_called
                bar_action_called = True
        b = Bar

    Foo().run(delegator.Argv(['foo', 'bar']))
    assert bar_action_called

    bar_action_called = False
    Foo().run(delegator.Argv(['foo', 'b']))
    assert bar_action_called

@nose.tools.raises(NotImplementedError)
def test_cant_use_class_for_storage():
    class Foo(Interface):
        @staticmethod
        def action(*args):
            raise Exception
    class Bar(Interface):
        @staticmethod
        def action(*args):
            raise NotImplementedError
        f = Foo
    class Baz(Interface):
        blah = Foo
    # this should call Bar.action, not Foo.action,
    # because it's only called blah by Baz.
    Bar().run(delegator.Argv(['bar', 'blah']))
