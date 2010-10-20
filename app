#!/usr/bin/env python

class App(Interface):
    Help = BuiltinHelp
    
    description = 'Prints "Hello World!"'
    def action(self, foo, bar=False, baz='hello'):
        print 'Hello World!'

    class generate(Interface):
        description = 'Lists generation commands'

        # does action need self?
        def action(self):
            print 'foo', 'bar', 'baz'

        # do you need to inherit from Interface?
        class Foo:
            def action(self): pass
        class Bar:
            def action(self): pass
        class Baz:
            def action(self): pass

    g = Generate

    class Migrate:
        controller = MigrateController

    # ./app M
    # not ./app m
    M = Migrate

class MigrateController(Controller):
    def foo(self, bar, baz): pass

    def bar(self, bar=False):
        print 'Hello from bar'



