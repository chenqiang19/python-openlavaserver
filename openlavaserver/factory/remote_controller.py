from openlavaserver.factory.abstract_factory import BaseController
import openlavaserver.exceptions as exceptions
from openlavaserver.utils.ssh_client import SshClient

__all__ = ('RemoteController',)

class RemoteController(BaseController):

    def __init__(self, session=None):
        super(RemoteController, self).__init__()
        if not session:
            raise exceptions.SessionError("Client input session is None.")
    
        self.client = SshClient(session)

    def get_client(self):
        return id(self.client)

    def get_shell_command_dict(self, command):
        lines = self.client.ssh_exec_command(command)
        if not lines:
            raise exceptions.SshExecuteError()
        lines_dict = super().convert_shell_stream_to_list(lines, command)
        return lines_dict

    def get_openlava_command_dict(self, command):
        lines = self.client.ssh_exec_command(command)
        if not lines:
            return lines
        lines_dict = super().convert_openlava_stream_to_dict(lines, command)
        return lines_dict