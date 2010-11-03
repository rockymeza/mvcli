#!/usr/bin/env python
from core.interface import Interface, InterfaceMeta, BuiltinHelp
import controller.main
import sys

__metaclass__ = InterfaceMeta
class App:
    description = 'This is my app'
    help = BuiltinHelp

    class M(controller.main.Main):
        description = 'This is M'

    @classmethod
    def action(cls):
        print cls.sub_commands

App().start(sys.argv)
