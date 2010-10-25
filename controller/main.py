from core.controllers import Controller

class Main(Controller):
    def main(self):
        print 'Hello World'

    def foo(self, bar, baz, qux, quux):
        print (bar, baz)

    def bar(self, *args):
        print (args)

