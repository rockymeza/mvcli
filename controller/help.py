from core import introspection
from core.formatter import color
from collections import namedtuple
from core.exceptions import *

Metadata = namedtuple('Metadata', 'description options examples')

class Help:
    actions = {}

    def __init__(self, request, config):
        self.request = request
        self.config = config
    
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

                    for attr in ['description']:
                        if hasattr(meta, attr):
                            out.append(attr.upper())
                            out.append('\t' + getattr(meta, attr))
                    
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
                    meta = self.actions[name]
                    for attr in ['description']:
                        if hasattr(meta, attr):
                            line += '\t\t' + getattr(meta, attr)
                    out.append(line)
                    
            print '\n'.join(out)

def action(cls, name, description, examples=None, options=None):
    cls.actions[name] = Metadata(description, options, examples or [])
    
        
        
Help.title = 'Help Controller'
Help.description = 'This is the awesome help controller'
action(Help, 'main', 'this is main')
action(Help, 'foo', 'foo description')
