from core.register import register_controller

class Main:
    def main(self):
        print 'wazzaa'

register_controller(Main, 'main', 'm')
