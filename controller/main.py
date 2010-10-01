from core.register import controller

@controller('main', 'm')
class Main:
    def main(self):
        print self.request['controller'], self.request['action']

