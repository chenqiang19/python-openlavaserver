
import websockets
import asyncio
import json
from websockets.legacy.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedError

from openlavaserver.handler.openlava_handler import OpenlavaHandler
from openlavaserver.handler.task_handler import TaskHandler
from openlavaserver.utils.apscheduler_util import TimeScheduler
from openlavaserver.config import CONF
from . import base

from openlavaserver.utils import log_util

_LOGGER = log_util.get_logger(__name__)

__all__ = ('WebsocketHandler', 'WebsocketServer', 'WebsocketAdapter',)

class WebsocketHandler(base.BaseHandler):

    def __init__(self):
        self._next_handler = None
    
    def set_next_handler(self, base_handler=None):
        self._next_handler = base_handler

    def handler(self, config=None, **kwargs):
        
        if 'invoker' not in kwargs.keys():
            raise ValueError("Invoker must not be None")
        
        invoker = kwargs.get('invoker')
        
        if not config:
            raise ValueError("Config must not be None")
        
        config_keys = config.keys()

        if "websocket" not in config_keys:
            raise ValueError("Websocket config item is not in yaml")
        
        if self._next_handler is not None:
            return self._next_handler.handler(config)

        return True, invoker


class WebsocketServer:

    def __init__(self, config=None, callback=None):
        
        if not config:
            raise ValueError("Worker is True, config not allow to be None")
        
        self._config = config.get('websocket')
        self._callback = callback
        self.message_dict = {}
        self.client = {}
    
    async def ws_send_message(self, client_name, message):
        websocket_client = self.client.get(client_name)
        if not websocket_client:
            await websocket_client.send(message)

    def commands_listener(self, event):
        if not event.exception:
            self.message_dict[event.job_id] = event.retval
            if len(self.message_dict) == 6:
                if len(self.client) == 0:
                    print(json.dumps(self.message_dict))
                else:
                    for name in self.client.keys():
                        self.ws_send_message(name, json.dumps(self.message_dict))
        else:
            _LOGGER.warning(str(event.exception))


    async def ws_receiver(self, websocket: WebSocketServerProtocol):
        async for message in websocket:
            result = None
            try:
                if message != "" and message is not None:
                    data = json.loads(message)
                    if 'client_name' in data:
                        client_name = data.get('client_name')
                        if client_name and client_name not in self.client:
                            self.client[client_name] = websocket
                    else:
                        raise ValueError('Client name is None')
                    result = self._callback(data)
                else:
                    await websocket.send("Message is None")
            except ConnectionClosedError as e:
                result = str(e)
                _LOGGER.warning(result)
                
            await websocket.send(json.dumps(result))

    async def ws_server(self):
        async with websockets.serve(self.ws_receiver, self._config.get("ip"), self._config.get("port")):
            await asyncio.Future()

class WebsocketAdapter:

    def __init__(self, scheduler=None):
        self.setup_handler = None
        self.websocket_server = None 
        if not scheduler:
            self.time_scheduler = TimeScheduler()
        else:
            self.time_scheduler = scheduler

    def _start_scheduler(self):
        self.time_scheduler.start()

    def _set_handler_chain(self):
        openlava_handler = OpenlavaHandler()
        task_handler = TaskHandler()
        websocket_handler = WebsocketHandler()

        openlava_handler.set_next_handler(task_handler)
        task_handler.set_next_handler(websocket_handler)

        self.setup_handler = openlava_handler

    def _listen_scheduler(self, listener):
        self.time_scheduler.add_listener(listener)

    def setup_websocket(self):
        self._set_handler_chain()
        
        if not self.setup_handler:
            raise ValueError("Websocket setup failed")

        handler_flag, invoker = self.setup_handler.handler(CONF.config)
        
        if handler_flag and invoker is not None:
            self.websocket_server = WebsocketServer(CONF.config, invoker.handler_commands)
            invoker.add_commands_timer(self.time_scheduler)
            invoker.batch_execute()
            self._listen_scheduler(self.websocket_server.commands_listener)
            self._start_scheduler()
            asyncio.run(self.websocket_server.ws_server())
            
