from core import introspection
from collections import namedtuple
import exceptions

Metadata = namedtuple('Metadata', 'description options examples')
class Controller:
    actions = {}

    def __init__(self, mvcli):
        self.mvcli = mvcli
        self.request = mvcli.request
        self.config = mvcli.config
        self.controllers = mvcli.controllers
        self.formatter = mvcli.formatter
    
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
                self.formatter.title(self.title)
                meta = self.actions[action]
                
                if meta.description:
                    self.formatter.header('DESCRIPTION:')
                    self.formatter.indent(meta.description)

                if meta.options:
                    self.formatter.header('OPTIONS:')
                    for name, description in meta.options.items():
                        self.formatter.definition(name, description)

                if meta.examples:
                    self.formatter.header('EXAMPLES:')
                    for example in meta.examples:
                        self.formatter.indent(example)
            else:
                raise exceptions.ActionError(action)    

    def controller_help(self):
        self.formatter.title(self.title)

        if hasattr(self, 'description'):
            self.formatter.header('DESCRIPTION:')
            self.formatter.indent(self.description)
        if self.actions:
            self.formatter.header('SUBCOMMANDS:')
            for name, method in self.actions.items():
                self.formatter.definition(name, self.actions[name].description)


class Help(Controller):
    def main(self):
        self.formatter.title(self.mvcli.title)
        
        if hasattr(self.mvcli, 'description'):
            self.formatter.header('DESCRIPTION:')
            self.formatter.indent(self.mvcli.description)

        for controller, routes in self.controllers.reverse_items():
            self.formatter.definition(', '.join(routes), controller.title)
