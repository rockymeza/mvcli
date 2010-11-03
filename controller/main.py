from core.controllers import Controller

def action(description):
    def f(function):
        function.is_action = True
        function.description = description
        return function
    return f

class Git(Interface):
    def prepare():
        self.api_obj = api.obj()
    def index():
        print 'You must specify a command'
    class Status:
        class SubStatus:
            
        def index():
            self.obj.git_status

class Main(Controller):
    
    @action('main description')
    def main(self):
        print 'Hello World'

    @action('foo description')
    def foo(self):
        print 'Hello World'

