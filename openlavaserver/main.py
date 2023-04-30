import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openlavaserver.config import CONF, configure
from openlavaserver.handler import WebsocketAdapter

def load_config():
    configure("openlavaserver")
    #print(CONF.config)

if __name__ == '__main__':

    #load config
    load_config()

    #setup websocket client
    ws_client = WebsocketAdapter()
    #ws_client.set_handler_chain()
    ws_client.setup_websocket()