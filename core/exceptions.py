class ControllerError(Exception): pass
class ActionError(Exception): pass
class OptionError(Exception): pass
class OptionValueError(Exception): pass
class NoFilesError(Exception): pass
class MissingOptionError(Exception):
    def __str__(self):
        if isinstance(self.value, list):
            if len(self.value) == 1:
                return self.value[0]
            else:
                last_item = self.value.pop()
                string = ', '.join(self.value)
                return string + ' and ' + last_item
        else:
            Exception.__str__()
