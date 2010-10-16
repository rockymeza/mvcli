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

