#!/usr/bin/env python
from core.interface import Interface, BuiltinHelp
import controller.main
import sys

class App(Interface):
    Help = BuiltinHelp
    
    description = 'Prints "Hello World!"'
    def action(app):
        print 'Hello World!'

    class generate(Interface):
        description = 'Lists generation commands'

        # does action need self?
        def action(app):
            print 'foo', 'bar', 'baz'

        # do you need to inherit from Interface?
        class Foo:
            def action(app): pass
        class Bar:
            def action(app): pass
        class Baz:
            def action(app): pass

    g = generate

    class Migrate:
        controller = controller.main.Main

    # ./app M
    # not ./app m
    M = Migrate



App().run(sys.argv)
