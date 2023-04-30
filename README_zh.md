
## Openlava Server


OpenLava是100%免费、开源、兼容IBM LSF的工作负载调度器，支持各种高性能计算和分析应用。

Openlava Server是为了更加方便的操作Openlava而提供的一套实现方式，其中实现了对Openlava的本地和远程操作模式、对Openlava调用结果的解析等功能。

#### Installation

确保你已经安装了pip（python包管理器）.

```
pip install openlava-server
```

#### Example

openlava-server使你能够更加简单的实现openlava的相应操作，并对结果进行解析和处理。

##### 1、 Local Module

```
import openlava-server

#导入本地控制器
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

#导入远程控制器
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
