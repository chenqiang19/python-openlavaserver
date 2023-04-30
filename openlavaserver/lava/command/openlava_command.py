import json
import re
import time

from openlavaserver.lava.command import base
import openlavaserver.exceptions as exceptions

__all__ = ('BHostCommand', 'LsHostCommand', 'BJobCommand', \
           'LsLoadCommand', 'BqueueCommand', 'BuserCommand', \
           'ShellCommand',)

def check_input_command(pattern, command):
    pattern = '^' + pattern
    ret = re.match(pattern, command)
    if not ret:
        return False
    return True

class ShellCommand(base.BaseModule):

    def __init__(
        self, 
        shell_receiver=None, 
        command=None, 
        name="shell", 
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):
        if not command:
            raise exceptions.ShellError("shell command is None")
        super(ShellCommand, self).__init__(command, name, status, job_time)
        self._shell_receiver = shell_receiver

    def execute(self):
        return self._shell_receiver.get_shell_stream(self.command)

class BJobCommand(base.BaseModule):

    def __init__(
        self, 
        job_receiver=None, 
        command='bjobs -u all', 
        name="bjobs", 
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):

        if check_input_command(name, command):
            super(BJobCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("job", "input job command is error", command)
        self._job_receiver = job_receiver

    def execute(self):
        return self._job_receiver.get_bjobs_stream(self.command)

class BHostCommand(base.BaseModule):

    def __init__(
        self, 
        host_receiver=None, 
        command='bhosts', 
        name="bhosts",
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):
        
        if check_input_command(name, command):
            super(BHostCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("host", "input host command is error", command)
        self._host_receiver = host_receiver

    def execute(self):
            return self._host_receiver.get_bhost_stream(self.command)

class LsHostCommand(base.BaseModule):

    def __init__(
        self, 
        host_receiver=None, 
        command='lshosts -w', 
        name="lshosts", 
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):

        if check_input_command(name, command):
            super(LsHostCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("host", "input host command is error", command)
            
        self._host_receiver = host_receiver

    def execute(self):
            return self._host_receiver.get_lshost_stream(self.command)

class LsLoadCommand(base.BaseModule):

    def __init__(
        self, 
        load_receiver=None, 
        command='lsload', 
        name="lsload", 
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):

        if check_input_command(name, command):
            super(LsLoadCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("load", "input load command is error", command)

        self._load_receiver = load_receiver

    def execute(self):
            return self._load_receiver.get_lsloads_stream(self.command)

class BqueueCommand(base.BaseModule):

    def __init__(
        self, 
        queue_receiver=None, 
        command='bqueues', 
        name="bqueues", 
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):

        if check_input_command(name, command):
            super(BqueueCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("queue", "input queue command is error", command)

        self._queue_receiver = queue_receiver

    def execute(self):
            return self._queue_receiver.get_bqueues_stream(self.command)

class BuserCommand(base.BaseModule):
    
    def __init__(
        self, 
        user_receiver=None, 
        command='busers all', 
        name="busers", 
        status=base.CommandStat.ACTIVE, 
        job_time=5,
    ):

        if check_input_command(name, command):
            super(BuserCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("user", "input user command is error", command)

        self._user_receiver = user_receiver

    def execute(self):
            return self._user_receiver.get_busers_stream(self.command)


class LsClustersCommand(base.BaseModule):

    def __init__(
        self,
        cluster_receiver=None,
        command='lsclusters',
        name="lscluster",
        status=base.CommandStat.ACTIVE,
        job_time=5,
    ):
        if check_input_command(name, command):
            super(LsClustersCommand, self).__init__(command, name, status, job_time)
        else:
            raise exceptions.OpenlavaError("cluster", "input cluster command is error", command)
    
        self._cluster_receiver = cluster_receiver

    def execute(self):
         return self._cluster_receiver.get_lscluster_stream(self.command)