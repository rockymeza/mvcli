from core import introspection
from core.formatter import color

class Main:
    title = 'Main Foo'
    description = 'This does not do anything'

    def __init__(self, request, config):
        self.request = request
        self.config = config
        self.actions = {}
    
    def main(self):
        """
        Description: Prints Hello World
        """
        print 'Hello World'

    def foo(self, bar, baz, qux, quux):
        print (bar, baz)

    def help(self):
        out = []
        out.append(color(Main.title, 'cyan'))

        if hasattr(Main, 'description'):
            out.append('DESCRIPTION:')
            out.append('\t' + Main.description)

        if hasattr(Main, 'usage'):
            out.append('USAGE:')
            out.append('t' + Main.usage)
        
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
        
        
        

