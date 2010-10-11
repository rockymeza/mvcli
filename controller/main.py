from core import introspection
from core.formatter import color

class Main:
    title = 'Foo Command'
    description = 'This does not do anything'

    def __init__(self, request, config):
        self.request = request
        self.config = config
        self.actions = {}
    
    def main(self):
        print 'Hello World'

    def foo(self, bar, baz, qux, quux):
        print (bar, baz)

    def help(self):
        print color(Main.title, 'cyan')

        if hasattr(Main, 'description'):
            print '\nDESCRIPTION:'
            print '\t' + Main.description

        if hasattr(Main, 'usage'):
            print '\nUSAGE:'
            print 't' + Main.usage
        
        actions = introspection.getactions(self)
        for name, method in actions:
            optionspec = introspection.getoptionspec(method)
            print optionspec
        
        
        

