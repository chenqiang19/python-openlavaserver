# -*- coding: utf-8 -*-
"""
The project uses the pytest testing framework. Some of the instructions are listed below.
If you want to test the whole .py file, you can use pytest xxx.py
If you want to test a TestClass, you can use pytest xxx.py::TestClass
If you want to test a method, you can use pytest xxx.py::TestClass::test_method
If you want to test a batch test cases:
    you must be install a plugin of pytest-xdist, pip install -U pytest-xdist
    then you can use this command, pytest xxx.py -n NUM
If you want to re-try some failure cases:
    you must bu install a plugin of pytest-rerunfailures
    then you can use this command, pytest xxx.py --reruns NUM
If you want to display the result of running, you can use pytest xxx.py -s
"""

import sys
import os
import pytest
import threading

from openlavaserver.lava import JobReceiver, CommandInvoker, HostReceiver, ShellReceiver
from openlavaserver.lava.command import BJobCommand, BHostCommand, ShellCommand
from openlavaserver.session import RemoteSession
from openlavaserver.factory import RemoteController, LocalController

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#print(sys.path)

from session import RemoteSession
from factory import LocalController, RemoteController

def create_remote_client():
    session = RemoteSession.SessionBuilder('10.62.4.10','gaotongliang', '1234').build()
    remote_controller = RemoteController(session)
    return remote_controller

@pytest.mark.skip
def test_remote_session():
    session = RemoteSession.SessionBuilder('10.62.4.10','gaotongliang', '1234').set_port(22).build()
    
    print(session)

@pytest.mark.local
def test_local_controller():

    local_controller = LocalController()

    lines_dict = local_controller.get_command_dict("ls")

    print(lines_dict)

@pytest.mark.remote
def test_remote_controller():
    client = create_remote_client()
    lines = client.get_command_dict("ls") 

    print("SSH result info:")
    print(lines)
    print(type(lines))

@pytest.mark.multi_thread
def test_multi_thread_singleton():
    task_list = []
    for _ in range(20):
        thread = threading.Thread(target=create_remote_client)
        task_list.append(thread)
    
    for _ in task_list:
        _.start()
    
    for _ in task_list:
        _.join()

@pytest.mark.job_command
def test_openlava_job_command():
    from lava import JobReceiver, OpenlavaInvoker, JobReceiver
    from lava import BJobCommand

    client = create_remote_client()
    openlava_invoker = OpenlavaInvoker()

    job_reciver = JobReceiver(client.get_command_dict)
    
    command = "ls -a"
    bjob_command = BJobCommand(job_reciver, command)

    lines = openlava_invoker.execute(bjob_command)
    print(lines)

@pytest.skip
def test_json_add_data():
    import json
    old = '{"status_code": 200, "data": {"key1": "value", "key2": "value", "key3": -5, "key4": "key5", "key6": [{"key7": 1542603600, "key8": 94}]}, "key9": "OK"}'
    new = json.dumps({"new_key": json.loads(old)})
    print(new)

@pytest.skip
def test_importlib_pkg():
    import importlib
    module = importlib.import_module("list_demo", package="test")
    list_module = getattr(module, "list_rules", [])
    print(module)
    print(list_module)

@pytest.mark.multi_user
def user_a():
    session = RemoteSession.SessionBuilder('192.20.4.200','root', 'smartcore.123').build()
    client = RemoteController(session)
    openlava_invoker = CommandInvoker()

    shell_receiver = ShellReceiver(client.get_shell_command_dict)
    
    command = "ls"
    shell_command = ShellCommand(shell_receiver, command)

    lines = openlava_invoker.execute(shell_command)
    print(lines)
    print(type(lines))
    print(lines.keys())

@pytest.mark.multi_user
def user_b():
    session = RemoteSession.SessionBuilder('10.62.4.10','gaotongliang', '1234').build()
    client = RemoteController(session)
    openlava_invoker = CommandInvoker()

    job_reciver = JobReceiver(client.get_openlava_command_dict)
    
    command = "pwd"
    bjob_command = BJobCommand(job_reciver, command)
    lines = openlava_invoker.execute(bjob_command)

    print(lines)

@pytest.mark.multi_commands
def check_multi_commands():
    client = LocalController()
    
    openlava_invoker = CommandInvoker()

    job_receiver = JobReceiver(client.get_openlava_command_dict)
    host_receiver = HostReceiver(client.get_openlava_command_dict)

    command_job = "ls"
    command_host = "pwd"
    
    bhost_command = BHostCommand(host_receiver, command_host)
    bjob_command = BJobCommand(job_receiver, command_job)

    openlava_invoker.add_command(bhost_command)
    openlava_invoker.add_command(bjob_command)
    results = openlava_invoker.batch_execute()
    
    print(results)

@pytest.mark.multi_user
def check_multi_user():
    task_list = []
    
    thread_a = threading.Thread(target=user_a)
    task_list.append(thread_a)
    thread_b = threading.Thread(target=user_b)
    task_list.append(thread_b)
    
    for _ in task_list:
        _.start()
    
    for _ in task_list:
        _.join()

@pytest.skip
def check_class_object():
    session1 = RemoteSession.SessionBuilder('192.20.4.200','root', 'smartcore.123').build()
    session2 = RemoteSession.SessionBuilder('10.62.4.10','gaotongliang', '1234').build()
    print(id(session1) == id(session2))
    client1 = RemoteController(session1)
    client2 = RemoteController(session2)
    print(id(client1)==id(client2))


#if __name__ == '__main__':
    #check_multi_commands()
    #check_multi_user()
    #check_class_object()
    #user_a()