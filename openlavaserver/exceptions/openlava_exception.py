from openlavaserver.exceptions import base

__all__ = ('OpenlavaError',)

class OpenlavaError(base.ClientException):
    message = "Openlava error"
    module = "plugin"

    def __init__(self, module=None, message=None, command=None):
        self.message = message or self.message
        self.module = module or self.module
        self.command = command
        formatted_string = "[%s]: %s" % (self.module, self.message)
        if self.command:
            formatted_string += " (Command is: %s)" % command
        super(OpenlavaError, self).__init__(formatted_string)
