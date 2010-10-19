from core import introspection
from core.formatter import color
from collections import namedtuple
import exceptions

Metadata = namedtuple('Metadata', 'description options examples')
class Controller:
    actions = {}

    def __init__(self, request, config, controllers):
        self.request = request
        self.config = config
        self.controllers = controllers
    
    @property
    def title(self):
        return self.__name__

    @classmethod
    def metadata(cls, title = None, description = None):
        cls.title = title
        cls.description = description

    @classmethod
    def action(cls, name, description, options=None, examples=None):
        cls.actions[name] = Metadata(description, options or {}, examples or [])

    def help(self, *actions):
        lines = self.action_help(*actions) if actions else self.controller_help()

    def action_help(self, *actions):
        for action in actions:
            if action in self.actions:
                self.ptitle(self.title)
                meta = self.actions[action]
                
                if meta.description:
                    self.pheader('DESCRIPTION:')
                    self.pindent(meta.description)

                if meta.options:
                    self.pheader('OPTIONS:')
                    for name, description in meta.options.items():
                        self.pdefinition(name, description)

                if meta.examples:
                    self.pheader('EXAMPLES:')
                    for example in meta.examples:
                        self.pindent(example)
            else:
                raise exceptions.ActionError(action)    

    def controller_help(self):
        lines = []
        self.ptitle(self.title)

        
        if hasattr(self, 'description'):
            self.pheader('DESCRIPTION:')
            self.pindent(self.description)
        if self.actions:
            self.pheader('SUBCOMMANDS:')
            for name, method in self.actions.items():
                self.pdefinition(name, self.actions[name].description)

    def ptitle(self, text):
        print color(text, self.config['colors.title'])

    def pheader(self, text):
        print color(text, self.config['colors.header'])
    
    def pindent(self, text):
        print '\t' + text

    def pdefinition(self, key, value):
        print color('\t' + key, self.config['colors.key']) + color('\t\t' + value, self.config['colors.value'])


class Help(Controller):
    def main(self):
        for controller, routes in self.controllers.reverse_items():
            self.pdefinition(', '.join(routes), controller.title)

    def help(self, *actions):
        lines = self.action_help(*actions) if actions else self.controller_help()

    def action_help(self, *actions):
        for action in actions:
            if action in self.actions:
                self.ptitle(self.title)
                meta = self.actions[action]
                
                if meta.description:
                    self.pheader('DESCRIPTION:')
                    self.pindent(meta.description)

                if meta.options:
                    self.pheader('OPTIONS:')
                    for name, description in meta.options.items():
                        self.pdefinition(name, description)

                if meta.examples:
                    self.pheader('EXAMPLES:')
                    for example in meta.examples:
                        self.pindent(example)
            else:
                raise exceptions.ActionError(action)    

    def controller_help(self):
        lines = []
        self.ptitle(self.title)

        
        if hasattr(self, 'description'):
            self.pheader('DESCRIPTION:')
            self.pindent(self.description)
        if self.actions:
            self.pheader('SUBCOMMANDS:')
            for name, method in self.actions.items():
                self.pdefinition(name, self.actions[name].description)
