from openlavaserver.exceptions import base

__all__ = ('ShellError',)

class ShellError(base.ClientException):
    message = "Session Error"
