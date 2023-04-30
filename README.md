
## Openlava Server


OpenLava is a 100% free, open source, IBM LSF compliant workload scheduler that supports a variety of high performance computing and analytics applications.

Openlava Server is a set of implementations provided for more convenient operation of Openlava, which implements functions such as local and remote operation modes and parsing of Openlava call results.

#### Installation

Make sure you have pip (python package manager) installed.

##### 1、python package install

```
pip install openlava-server
```
##### 2、source resource install
```
# download source resource
git clone xxxx.git
# install dependencies
python -m pip install --upgrade setuptools wheel
# packaging
python setup.py sdist bdist_wheel
# install .whl
cd dist && pip install ./openlava_server-1.0.0-py3-none-any.whl
```

#### Example

openlava-server enables you to more easily implement openlava's corresponding operations, and parse and process the results.

##### 1、 Local Module

```
import openlava-server

#import local controller
from openlava-server.factory import LocalController
from openlava-server.lava import JobReceiver, OpenlavaInvoker
from openlava-server.lava.command import BJobCommand

client = LocalController()

openlava_invoker = OpenlavaInvoker()

job_receiver = JobReceiver(client.get_command_dict)

bjob_command = BJobCommand(job_receiver)

lines = openlava_invoker.execute(bjob_command)
```

##### 2、 Remote Module

```
import openlava-server

#import remote controller
from openlava-server.factory import RemoteController
from openlava-server.lava import JobReceiver, OpenlavaInvoker
from openlava-server.lava.command import BJobCommand
from session import RemoteSession

session = RemoteSession.SessionBuilder('10.62.4.10','gaotongliang', '1234').build()

client = RemoteController(session)

openlava_invoker = OpenlavaInvoker()

job_reciver = JobReceiver(client.get_command_dict)

bjob_command = BJobCommand(job_reciver)

lines = openlava_invoker.execute(bjob_command)
```

##### 3、 Batch Execute Module

```
import openlava-server

from openlava-server.factory import RemoteController
from openlava-server.lava import JobReceiver, OpenlavaInvoker, HostReceiver
from openlava-server.lava.command import BJobCommand, BHostCommand
from session import RemoteSession

session = RemoteSession.SessionBuilder('10.62.4.10','gaotongliang', '1234').build()

client = RemoteController(session)

openlava_invoker = OpenlavaInvoker()

job_reciver = JobReceiver(client.get_command_dict)
host_receiver = HostReceiver(client.get_command_dict)

bjob_command = BJobCommand(job_reciver)
bjob_command = BJobCommand(job_receiver)

openlava_invoker.add_command(bhost_command)
openlava_invoker.add_command(bjob_command)
results = openlava_invoker.batch_execute()
```

##### 4、 Websocket Setup Methos

```
from openlavaserver.config import configure
from openlavaserver.handler import WebsocketAdapter

configure("openlavaserver")
ws_client = WebsocketAdapter()
ws_client.set_handler_chain()
ws_client.setup_websocket()
```
