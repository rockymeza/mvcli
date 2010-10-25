import re
import delegator

class InterfaceMeta(type):
    def __new__(cls, name, bases, dict):
        # All we do is make sure our classes inherit from Interface
        try:
            if Interface not in bases:
                bases = bases + (Interface,)
        except NameError:
            # Interface is not defined yet. Likely, we are creating it right now
            pass
        return super(InterfaceMeta, cls).__new__(cls, name, bases, dict)

    def __init__(cls, name, bases, dict):
        cls.sub_commands = []
        cls.responds_to_res = []
        for (name, prop) in dict.items():
            if isinstance(prop, InterfaceMeta):
                # Nested class. Treat it as a subcommand.
                cls.add_command(name, prop)
            elif isinstance(prop, type(lambda:1)):
                # A function. Make it a staticmethod
                setattr(cls, name, staticmethod(prop))
        for command in cls.sub_commands:
            command.use_parent(cls)

class Interface(object):
    __metaclass__ = InterfaceMeta
    @classmethod
    def use_name(cls, name):
        """
        This is a hook to allow an Interface to learn
        what it is called in the outer class. By default,
        make sure we have a name attribute, and add the name
        to the list of regexes we respond to.
        """
        try:
            cls.name
        except AttributeError:
            cls.name = slugify(name)
        cls.responds_to_res.append(re.compile('^' + slugify(name) + '$'))

    @classmethod
    def use_parent(cls, parent):
        """
        This is a hook to allow an Interface to access its parent,
        in order to allow magic. By default, we don't do anything.
        """
        pass

    @classmethod
    def add_command(cls, name, command):
        command.use_name(name)
        cls.sub_commands.append(command)

    @classmethod
    def responds_to(cls, argv):
        """
        True if we want to handle this request, False otherwise.
        By default, treat our name as a regex and match the first
        element of argv.
        """
        if not argv:
            return False
        else:
            for pat in cls.responds_to_res:
                if pat.match(argv[0]):
                    return True
        return re.compile(cls.name).match(argv[0])

    @classmethod
    def consume(cls, argv):
        """
        How much of argv did we actually use?
        With the default responds_to, we used the
        first element.
        """
        argv.pop(0)

    @classmethod
    def get_sub_commands(cls):
        """
        Iterate through all possible subcommands,
        including inherited ones, in MRO order.
        """
        for parent in cls.__mro__:
            try:
                s = parent.sub_commands
            except AttributeError:
                # Not an interface, skip.
                pass
            else:
                for command in s:
                    yield command

    @classmethod
    def run(cls, argv):
        cls.consume(argv)

        # Offer to let the controller handle it.
        try:
            return cls.controller.run(argv)
        except (AttributeError, NotImplementedError):
            # Either we don't have a controller,
            # or the controller doesn't want to handle
            # the request. Keep going.
            pass

        # Next, check all the sub commands.
        for command in cls.get_sub_commands():
            if command.responds_to(argv):
                return command.run(argv)

        # No subcommands respond to this request.
        # The action method is our last resort.
        optionspec = delegator.getoptionspec(cls.action)
        arguments = delegator.parse_options(optionspec, delegator.Argv(argv))
        return cls.action(*arguments.args, **arguments.kwargs)

    @classmethod
    def action(cls):
        """
        If our subclass lets a request fall through to action,
        but doesn't provide their own, we have no way of handling
        the request.
        """
        raise NotImplementedError

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
                if (not name) or command.responds_to([name]):
                    print command.name, command.description

        @classmethod
        def use_parent(cls, parent):
            cls.parent = parent
            for command in parent.sub_commands:
                if not isinstance(command, BuiltinHelpMeta):
                    sub_help = BuiltinHelp()
                    command.add_command(cls.name, sub_help)
                    sub_help.use_parent(command)
    return Help

def slugify(str):
    """
    camel case string -> slug
    """
    if str.islower():
        return str
    return '-'.join([i.lower() for i in re.compile('[A-Z][a-z]*').findall(str)])


#__metaclass__ = InterfaceMeta
#class App:
#    help = BuiltinHelp()
#    description = 'an app'
#    class Foo:
#        description = 'foo: prints some stuff'
#        def action(*args):
#            print 'App.Foo.action', args
#        class Bar:
#            description = 'foo bar: asdf'
#import sys
#import copy
#App.run(copy.copy(sys.argv))
