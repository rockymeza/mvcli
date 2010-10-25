import re
import delegator

class InterfaceMeta(type):
    def __new__(cls, name, bases, dict):
        return super(InterfaceMeta, cls).__new__(cls, name, bases + (Interface,), dict)

    def __init__(cls, name, bases, dict):
        cls.sub_commands = []
        for (name, prop) in dict.items():
            if isinstance(prop, InterfaceMeta):
                cls.add_command(name, prop)
            elif isinstance(prop, type(lambda:1)):
                setattr(cls, name, staticmethod(prop))
        for command in cls.sub_commands:
            command.use_parent(cls)

class Interface(object):
    @classmethod
    def use_name(cls, name):
        try:
            cls.name
        except AttributeError:
            cls.name = re.compile('^' + slugify(name) + '$')

    @classmethod
    def add_command(cls, name, command):
        command.use_name(name)
        cls.sub_commands.append(command)

    @classmethod
    def responds_to(cls, argv):
        return argv and cls.name.match(argv[0])

    @classmethod
    def consume(cls, argv):
        argv.pop(0)

    @classmethod
    def run(cls, argv):
        cls.consume(argv)
        for command in cls.sub_commands:
            if command.responds_to(argv):
                return command.run(argv)
        optionspec = delegator.getoptionspec(cls.action)
        arguments = delegator.parse_options(optionspec, delegator.Argv(argv))
        return cls.action(*arguments.args, **arguments.kwargs)

    @classmethod
    def use_parent(*args):
        pass

class BuiltinHelpMeta(InterfaceMeta):
    pass

def BuiltinHelp():
    class Help:
        __metaclass__ = BuiltinHelpMeta

        description = 'help <topic>: prints help about topic'
        @classmethod
        def action(cls, *names):
            (name,) = names or [None]
            if not name:
                print cls.parent.description
            for command in cls.parent.sub_commands:
                if (not name) or command.name.match(name):
                    print command.name.pattern, command.description

        @classmethod
        def use_parent(cls, parent):
            cls.parent = parent
            for command in parent.sub_commands:
                if not isinstance(command, BuiltinHelpMeta):
                    sub_help = BuiltinHelp()
                    command.add_command("^help$", sub_help)
                    sub_help.use_parent(command)
    return Help

def slugify(str):
    """
    camel case string -> slug
    """
    if str.islower():
        return str
    return '-'.join([i.lower() for i in re.compile('[A-Z][a-z]*').findall(str)])


__metaclass__ = InterfaceMeta
class App:
    help = BuiltinHelp()
    description = 'an app'
    class Foo:
        description = 'foo: prints some stuff'
        def action(*args):
            print 'App.Foo.action', args
        class Bar:
            description = 'foo bar: asdf'
import sys
import copy
App.run(copy.copy(sys.argv))
