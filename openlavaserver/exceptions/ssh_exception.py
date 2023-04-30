from openlavaserver.exceptions import base

__all__ = ('SshError', 'SshConnectError', 'SshExecuteError')

class SshError(base.ClientException):
    message = "SSH error"

class SshConnectError(SshError):
    message = "SSH connect error"

class SshExecuteError(SshError):
    message = "SSH execute command error"


