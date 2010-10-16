from core import introspection
from core.formatter import color

class Help:
    title = 'Help Controller'
    description = 'This does not do anything'

    def __init__(self, request, config):
        self.request = request
        self.config = config
        self.actions = {}
    
    def main(self):
        """
        Description: Prints app-wide help
        """
        print 'Hello World'

    def foo(self, bar, baz, qux, quux):
        print (bar, baz)

    def help(self, *actions):
        if actions:
            for action in actions:
                if hasattr(self, action):
                    method = getattr(self, action)
                    out = []
                    out.append(color(self.title + '#' + action, 'cyan'))
                    meta = introspection.getmeta(method)

                    for attr in ['description']:
                        if attr in meta:
                            out.append(attr.upper())
                            out.append('\t' + meta[attr])
                    
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
            
            actions = introspection.getactions(self)
            if actions:
                out.append('SUBCOMMANDS:')
                for name, method in actions.items():
                    line = '\t' + color(name, 'yellow')
                    meta = introspection.getmeta(method)
                    if 'description' in meta:
                        line += '\t' + meta['description']
                    out.append(line)
                    
            print '\n'.join(out)
        
        
        

