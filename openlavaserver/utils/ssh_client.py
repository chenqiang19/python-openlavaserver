from signal import raise_signal
import threading
import sys
import os
import paramiko
import functools

# from retrying import retry

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
#                 '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                '..')))

import exceptions
from openlavaserver.utils import log_util

_LOGGER = log_util.get_logger(__name__)

GLOBAL_SSH_USER_MAP = {}

def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    
    return synced_func

def check_repeated(session=None):
    ip = session.get_hostname()
    username = session.get_username()
    if not GLOBAL_SSH_USER_MAP.get(username):
        return False
    else:
        return True

def Singleton(cls):
    instances = {}

    @synchronized
    def get_instance(session=None):
        if not session:
            raise exceptions.SessionParamsError()
        key = session.get_hostname()
        if key not in instances.keys() and not check_repeated(session):
            instances[key] = cls(session)
            GLOBAL_SSH_USER_MAP[session.get_username()] = key
        return instances[key]
    
    return get_instance


@Singleton
class SshClient():

    def __init__(self, session=None):
        self.client = paramiko.SSHClient()
        self._session = session
        self.__create_ssh_client()

    def __create_ssh_client(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()
        try:
            self.client.connect(self._session.get_hostname(), 
                                username=self._session.get_username(),
                                password=self._session.get_password())
        except Exception as e:
            _LOGGER.warning(str(e))
            raise exceptions.SshConnectError(str(e))
    
    def ssh_exec_command(self, command=None):
        if not command:
            return None
        stdin, stdout, stderr = self.client.exec_command(command)
        stdout, stderr = stdout.readlines(), stderr.read()

        res = stdout if stdout is not None or stderr == b'' else stderr
        
        if isinstance(res, list):
            if len(res) == 0:
                res = b''.decode()
            return res

        return res.decode()

    def __del__(self):
        """Clean up resources on delete."""
        if self.client:
            # If we created a ssh client, try to close it out correctly
            try:
                self.client.close()
            except Exception as e:
                _LOGGER.warning(str(e))
            finally:
                self.client = None
                
                if GLOBAL_SSH_USER_MAP is not None and \
                        self._session.get_username() in GLOBAL_SSH_USER_MAP.keys():
                    del GLOBAL_SSH_USER_MAP[self._session.get_username()]

if __name__ == '__main__':
    from session import RemoteSession
    from factory import RemoteController
    session = RemoteSession.SessionBuilder('192.20.4.200','root','smartcore.123') \
                           .build()
    
    remote_controller = RemoteController(session)
