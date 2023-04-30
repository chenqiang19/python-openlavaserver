
from . import base
from openlavaserver.factory import LocalController, RemoteController
from openlavaserver.session import RemoteSession

__all__ = ('OpenlavaHandler',)

class OpenlavaHandler(base.BaseHandler):

    def __init__(self):
        self._next_handler = None
        self.client = None

    def set_next_handler(self, base_handler=None):
        self._next_handler = base_handler

    def get_client(self):
        return self.client

    def handler(self, config=None, **kwargs):

        if not self._next_handler:
            raise ValueError("Handler must not be None")
        
        if not config:
            raise ValueError("Config must not be None")
        
        config_keys = config.keys()

        if "openlava" not in config_keys:
            raise ValueError("Openlava config item is not in yaml")
        
        openlava_config = config.get("openlava")
        model = openlava_config.get("model")

        if model == "local":
            self.client = LocalController()
        elif model == "remote":
            hostname = openlava_config["host_name"]
            username = openlava_config["user_name"]
            password = openlava_config["password"]
            port = None
            if 'port' in openlava_config:
                port = openlava_config["port"]

            session = RemoteSession.SessionBuilder(hostname, username, password).set_port(port).build()
            try:
                self.client = RemoteController(session)
            except Exception as e:
                raise RuntimeError(str(e))

        return self._next_handler.handler(config, client=self.client)

