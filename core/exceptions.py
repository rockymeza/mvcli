class ControllerError(Exception):
    def __init__(self, controller):
        self.controller = controller

    def __str__(self):
        return repr(self.controller)
        
class ActionError(Exception):
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return repr(self.action)
        
class OptionError(Exception):
    def __init__(self, option):
        self.option = option

    def __str__(self):
        return repr(self.option)
        
class OptionValueError(Exception):
    def __init__(self, option):
        self.option = option

    def __str__(self):
        return repr(self.option)

class MissingOptionError(Exception):
    def __init__(self, option):
        self.option = option

    def __str__(self):
        if isinstance(self.option, list):
            if len(self.option) == 1:
                return self.option[0]
            else:
                last_item = self.option.pop()
                string = ', '.join(self.option)
                return string + ' and ' + last_item
        else:
            return repr(self.option)
