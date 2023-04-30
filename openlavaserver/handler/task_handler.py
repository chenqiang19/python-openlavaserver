
from openlavaserver.lava.command.openlava_command import BHostCommand, BJobCommand, BqueueCommand, BuserCommand, LsClustersCommand, LsLoadCommand, ShellCommand
from openlavaserver.lava.receiver.openlava_receiver import ClusterReceiver, HostReceiver, JobReceiver, LoadReceiver, QueueReceiver, ShellReceiver, UserReceiver
from openlavaserver.lava import CommandInvoker
from . import base

import re

__all__ = ('TaskHandler',)

class TaskEntity:

    def __init__(self, **entities):
        self.__dict__.update(entities)


class TaskHandler(base.BaseHandler):

    def __init__(self):
        self._next_handler = None
        self.invoker = None
        self.task_entities = []

    def set_next_handler(self, base_handler=None):
        self._next_handler = base_handler

    def get_invoker(self):
        return self.invoker 

    def convert_to_entity(self, task_list=None):
        entity = {}
        for task in task_list:
            for item in task.items():
                entity["name"] = item[0]
                params = item[1]
                for param in params:
                    if "command" in param.keys():
                        entity["command"] = param.get("command")
                    if "time" in param:
                        entity["time"] = param.get("time")
            task_entity = TaskEntity(**entity)
            self.task_entities.append(task_entity)
            entity.clear()

    def load_commands(self, client=None):
        if len(self.task_entities) > 0:
            command = None
            for entity in self.task_entities:
                if hasattr(entity, 'name'):
                    if re.search(entity.name.lower(), 'bjobs', re.IGNORECASE):
                        job_receiver = JobReceiver(client.get_openlava_command_dict)
                        if hasattr(entity, 'command'):
                            command = BJobCommand(job_receiver, entity.command)
                        else:
                            command = BJobCommand(job_receiver)
                    elif re.search(entity.name.lower(), 'bhosts', re.IGNORECASE):
                        host_receiver = HostReceiver(client.get_openlava_command_dict)
                        if hasattr(entity, 'command'):
                            command = BHostCommand(host_receiver, entity.command)
                        else:
                            command = BHostCommand(host_receiver)
                    elif re.search(entity.name.lower(), 'bqueues', re.IGNORECASE):
                        queue_receiver = QueueReceiver(client.get_openlava_command_dict)
                        if hasattr(entity, 'command'):
                            command = BqueueCommand(queue_receiver, entity.command)
                        else:
                            command = BqueueCommand(queue_receiver)
                    elif re.search(entity.name.lower(), 'SHELL', re.IGNORECASE):
                        shell_receiver = ShellReceiver(client.get_shell_command_dict)
                        if hasattr(entity, 'command'):
                            command = ShellCommand(shell_receiver, entity.command)
                        else:
                            command = ShellCommand(shell_receiver)
                    elif re.search(entity.name.lower(), 'lsclusters', re.IGNORECASE):
                        cluster_receiver = ClusterReceiver(client.get_openlava_command_dict)
                        if hasattr(entity, 'command'):
                            command = LsClustersCommand(cluster_receiver, entity.command)
                        else:
                            command = LsClustersCommand(cluster_receiver)
                    elif re.search(entity.name.lower(), 'lsload', re.IGNORECASE):
                        load_receiver = LoadReceiver(client.get_openlava_command_dict)
                        if hasattr(entity, 'command'):
                            command = LsLoadCommand(load_receiver, entity.command)
                        else:
                            command = LsLoadCommand(cluster_receiver)
                    elif re.search(entity.name.lower(), 'busers', re.IGNORECASE):
                        user_receiver = UserReceiver(client.get_openlava_command_dict)
                        if hasattr(entity, 'command'):
                            command = BuserCommand(user_receiver, entity.command)
                        else:
                            command = BuserCommand(user_receiver)
                    else:
                        raise ValueError("Input command is not support")
                    
                    if command is not None:
                        self.invoker.add_command(command)

    def handler(self, config=None, **kwargs):
        if 'client' not in kwargs.keys():
            raise ValueError("Client must not be None")

        client = kwargs.get('client')

        if not self._next_handler:
            raise ValueError("Handler must not be None")
        
        if not config:
            raise ValueError("Config must not be None")
        
        config_keys = config.keys()

        if "task" not in config_keys:
            raise ValueError("Task config item is not in yaml")
        
        task_list = config.get("task")

        if len(task_list) == 0:
            raise ValueError("Task must not be empty")

        self.convert_to_entity(task_list)
        
        self.invoker = CommandInvoker()
        
        self.load_commands(client)

        return self._next_handler.handler(config, invoker=self.invoker)