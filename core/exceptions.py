class MVCLIException(Exception): pass
class ControllerError(MVCLIException): pass
class ActionError(MVCLIException): pass
class OptionError(MVCLIException): pass
class OptionValueError(MVCLIException): pass
class NoFilesError(MVCLIException): pass
class MissingOptionError(MVCLIException):
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
