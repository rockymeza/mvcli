from core import introspection
from core.formatter import color
from collections import namedtuple
from core.exceptions import *

Metadata = namedtuple('Metadata', 'description options examples')
class Controller:
    actions = {}

    def __init__(self, request, config):
        self.request = request
        self.config = config
    
    @property
    def title(self):
        return self.__name__

    @classmethod
    def metadata(cls, title = None, description = None):
        cls.title = title
        cls.description = description


    def main(self):
        print 'Hello World'

    def foo(self, bar, baz, qux, quux):
        print (bar, baz)

    def help(self, *actions):
        if actions:
            for action in actions:
                if action in self.actions:
                    method = getattr(self, action)
                    out = []
                    out.append(color(self.title + '#' + action, 'cyan'))
                    meta = self.actions[action]
                    
                    if meta.description:
                        out.append('DESCRIPTION:')
                        out.append('\t' + meta.description)

                    if meta.options:
                        out.append('OPTIONS:')
                        for name, description in meta.options.items():
                            out.append('\t' + color(name, 'yellow') + '\t\t' + description)

                    if meta.examples:
                        out.append('EXAMPLES:')
                        for example in meta.examples:
                            out.append('\t' + example)

                    print '\n'.join(out)
                else:
                    raise ActionError(action)    
        else:
            out = []
            out.append(color(self.title, 'cyan'))

            for attr in ['description']:
                if hasattr(self, attr):
                    out.append(attr.upper())
                    out.append('\t' + getattr(self, attr))
            
            if self.actions:
                out.append('SUBCOMMANDS:')
                for name, method in self.actions.items():
                    line = '\t' + color(name, 'yellow')
                    line += '\t\t' + self.actions[name].description
                    out.append(line)
                    
            print '\n'.join(out)

    @classmethod
    def action(cls, name, description, options=None, examples=None):
        cls.actions[name] = Metadata(description, options or {}, examples or [])
