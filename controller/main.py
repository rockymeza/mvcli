class Main:
    def __init__(self, request, config):
        self.request = request
        self.config = config
        self.actions = {}
    
    def main(self):
        return 'Hello World'

    def foo(self, bar, baz = False):
        pass

