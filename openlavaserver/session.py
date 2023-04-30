import openlavaserver.exceptions as exceptions

DEFAULT_REMOTE_PORT = 22

class RemoteSession(object):

    def __init__(self, builder):
        self.username = builder._username
        self.password = builder._password
        self.port = builder._port
        if not self.port:
            self.port = DEFAULT_REMOTE_PORT
        self.hostname = builder._hostname
    
    def __str__(self):
        return "username:{}, password:{}, hostname:{}, port:{}".format(
            self.username, self.password, self.hostname, self.port)

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

    def get_hostname(self):
        return self.hostname
    
    def get_port(self):
        return self.port
    
    def check_session(self):
        if self.get_hostname != '' and self.get_username != '' and self.get_password != '' and self.get_port != '':
            return True
        return False

    class SessionBuilder:
        def __init__(self, 
                     hostname=None, 
                     username=None, 
                     password=None
                    ):
            if not username or not password or not hostname:
                raise exceptions.SessionParamsError("input error")
            self._username = username
            self._password = password
            self._hostname = hostname
            self._port = ""

        def set_port(self, port):
            if not port:
                self.port = DEFAULT_REMOTE_PORT
            self._port = port
            return self
        
        def build(self):
            return RemoteSession(self)
        