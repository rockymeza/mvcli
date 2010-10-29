import re
import delegator
from util import slugify

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
        for (name, prop) in dict.items():
            if isinstance(prop, InterfaceMeta):
                # Nested class.
                obj = prop(name, cls) # instatiate the interface
                cls.sub_commands.append(obj)
                setattr(cls, name, obj)

class Interface(object):
    __metaclass__ = InterfaceMeta
    def __init__(self, name = None, parent = None):
        self.parent = parent
        self.name = name
        if name:
            self.name_re = re.compile('^%s$' % slugify(name))

    def responds_to(self, argv):
        """
        True if we want to handle this request, False otherwise.
        By default, treat our name as a regex and match the first
        element of argv.
        """
        if not argv:
            return False
        else:
            return self.name_re.match(argv[0])

    def consume(self, argv):
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

    def run(self, argv):
        self.consume(argv)

        # Offer to let the controller handle it.
        try:
            return self.controller.run(argv)
        except (AttributeError, NotImplementedError):
            # Either we don't have a controller,
            # or the controller doesn't want to handle
            # the request. Keep going.
            pass

        # Next, check all the sub commands.
        for command in self.get_sub_commands():
            if command.responds_to(argv):
                return command.run(argv)

        # No subcommands respond to this request.
        # The action method is our last resort.
        optionspec = delegator.getoptionspec(self.action)
        arguments = delegator.parse_options(optionspec, delegator.Argv(argv))
        return self.action(*arguments.args, **arguments.kwargs)

    def action(self):
        """
        If our subclass lets a request fall through to action,
        but doesn't provide their own, we have no way of handling
        the request.
        """
        raise NotImplementedError
    
    def __repr__(self):
        return 'Interface_%s(%s, %s)' % (self.__class__.__name__, self.name, self.parent)

class BuiltinHelp(Interface):
    def __init__(self, *args, **kwargs):
        super(BuiltinHelp, self).__init__(*args, **kwargs)
        for command in self.parent.sub_commands:
            if not isinstance(command, BuiltinHelp):
                sub_help = BuiltinHelp(self.name, command)
                command.sub_commands.append(sub_help)

    description = 'help <topic>: prints help about topic'
    def action(self, *names):
        (name,) = names or [None]
        if not name:
            print self.parent.description
        for command in self.parent.sub_commands:
            if (not name) or command.responds_to([name]):
                print command.name, command.description


#__metaclass__ = InterfaceMeta
#class App:
#    help = BuiltinHelp
#    description = 'an app'
#    class Foo:
#        description = 'foo: prints some stuff'
#        def action(self, *args):
#            print 'App.Foo.action', args
#        class Bar:
#            description = 'foo bar: asdf'
#import sys
#import copy
#App().run(copy.copy(sys.argv))
