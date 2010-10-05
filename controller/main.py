from core.register import controller

@controller('main', 'm')
class Main:
    def __init__(self, request, config):
        self.request = request
        self.config = config
    def main(self):
        print self.request['controller'], self.request['action']

