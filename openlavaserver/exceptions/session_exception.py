from openlavaserver.exceptions import base

__all__ = ('SessionError', 'SessionParamsError',)

class SessionError(base.ClientException):
    message = "Session Error"

class SessionParamsError(SessionError):
    message = "Input session parameters are error"