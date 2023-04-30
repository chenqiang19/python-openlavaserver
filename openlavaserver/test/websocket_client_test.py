import asyncio
import json
from websockets import connect

#json command status (CHANGE, ACTIVE, INACTIVE)

def ws_single_json():
    openlava_json = """{
        "client_name": "user1"
        "name": "shell",
        "status": "UPDATE",
        "command": "dir",
        "time": 3
    }"""

    return json.loads(openlava_json)

def ws_batch_json():
    batch_json = """{
        "request_list": [{
            "name": "shell"
            "status": "CHANGE",
            "command": "pwd",
            "time": 3
        },{
            "name": "shell"
            "status": "CHANGE",
            "command": "pwd",
            "time": 3
        }]
    }"""
    return json.loads(batch_json)

def ws_none():
    return 'query_all_result'

#timeout in seconds
timeout = 10

async def hello(uri):
    async with connect(uri, ping_interval=20, ping_timeout=20) as websocket:
        await websocket.send(json.dumps(ws_none()))
        while(True):
            msg = await websocket.recv()
            print(msg)

asyncio.run(hello("ws://localhost:8080"))