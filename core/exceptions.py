class MVCLIException(Exception): pass
class ControllerError(MVCLIException): pass
class ActionError(MVCLIException): pass
class OptionError(MVCLIException): pass
class OptionValueError(MVCLIException): pass
class NoFilesError(MVCLIException): pass
class MissingOptionError(MVCLIException):
    def __str__(self):
        value = self.args[0]
        if isinstance(value, list):
            if len(value) == 1:
                return value[0]
            else:
                last_item = value.pop()
                string = ', '.join(value)
                return string + ' and ' + last_item
        else:
            Exception.__str__()
