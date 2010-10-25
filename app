#!/usr/bin/env python
from core.interface import Interface, InterfaceMeta, BuiltinHelp
import controller.main
import sys

__metaclass__ = InterfaceMeta
class App:
    description = 'This is my app'
    help = BuiltinHelp()

    class M:
        description = 'This is M'
        controller = controller.main.Main

    @classmethod
    def action(cls):
        print cls.sub_commands

App.run(sys.argv)
