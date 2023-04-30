import os

from openlavaserver.factory.abstract_factory import BaseController

__all__ = ('LocalController',)

class LocalController(BaseController):

    def __init__(self):
        super(LocalController, self).__init__()
        self.lines_dict = None

    def get_shell_command_dict(self, command):

        with os.popen(command, "r") as pipe_file:
            lines = pipe_file.readlines()
            self.lines_dict = super().convert_shell_stream_to_list(lines, command)
            return self.lines_dict
    
    def get_openlava_command_dict(self, command):

        with os.popen(command, "r") as pipe_file:
            lines = pipe_file.readlines()
            self.lines_dict = super().convert_openlava_stream_to_dict(lines, command)
            return self.lines_dict