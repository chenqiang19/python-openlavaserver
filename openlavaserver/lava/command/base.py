from enum import Enum, unique
import time
import json

LOCAT_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class ExendedEnum(Enum):

    @staticmethod
    def list(cls):
        return list(map(lambda c : c.name, cls)) #c.name, c.value

@unique
class CommandStat(str, ExendedEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UPDATE = "UPDATE"
    ERROR = "ERROR"

    def __str__(self):
        return self.value

class BaseModule(object):

    def __init__(self, command=None, name=None, status=None, job_time=None):
        self.name = name
        self.command = command
        self.status = CommandStat(status)
        self.create_at = time.strftime(LOCAT_TIME_FORMAT, time.localtime())
        self.update_at = None
        self.job_time = job_time

    def get_command(self):
        return self.command

    def get_name(self):
        return self.name
    
    def get_status(self):
        return CommandStat.ERROR
    
    def set_status(self, status):
        if CommandStat(status) not in CommandStat.__members__:
            return CommandStat.ERROR
        if CommandStat(status) == CommandStat.UPDATE:
            self.update_at = time.strftime(LOCAT_TIME_FORMAT, time.localtime())
            return CommandStat.UPDATE
        
        self.status = CommandStat(status)
        return CommandStat.ACTIVE if CommandStat(status) == CommandStat.ACTIVE else CommandStat.INACTIVE

    def check_status(self):
        return False if self.status == CommandStat.INACTIVE else True

    def execute(self):
        pass

    def __iter__(self):
        yield from {
            "name": self.name,
            "status": self.status,
            "command": self.command,
            "create_at": self.create_at,
            "update_at": self.update_at if self.update_at is not None else '',
            "job_time": self.job_time
        }.items()
    
    def __str__(self) -> str:
        return json.dumps(dict(self), ensure_ascii=False)
    
    def __repr__(self) -> str:
        return self.__str__()
