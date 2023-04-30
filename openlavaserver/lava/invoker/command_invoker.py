__all__ = ('CommandInvoker',)

class CommandInvoker():

    def __init__(self):
        self.command_dict = {}
        self.batch_result = {}
        self.scheduler = None
 
    def add_command(self, command):
        if command is not None:
            self.command_dict[command.get_name()] = command
    
    def clear_commands(self):
        self.command_dict.clear()
    
    def get_command(self, name):
        if name in self.command_dict:
            return self.command_dict.get(name)
        return None

    def add_commands_timer(self, scheduler=None):
        if not self.scheduler:
            self.scheduler = scheduler
        for name, command in self.command_dict.items():
            self.scheduler.add_job(name, command.execute)

    def update_command(self, command_json):
        command = self.get_command(command_json.get('name'))
        if command is not None:
            ret = command.set_status(command_json.get('status'))
            if ret.value == 'ERROR':
                raise ValueError('Command update error')
            setattr(command, 'command', command_json.get('command'))
            setattr(command, 'time', command_json.get('time'))

    #1、找到对应的command类
    #2、根据状态对command进行编辑
    #3、初始化的时候已经添加了conf中的默认command
    #4、websockets通信获取现有command的返回结果
    #   4.1 web请求单独的command
    #   4.2 web对command进行增删改查
    def handler_commands(self, json_message=None):
        if isinstance(json_message, dict):
            self.update_command(json_message)
        elif isinstance(json_message, list):
            request_json = json_message.get('request_json')
            for json in request_json:
                self.update_command(json)
        elif isinstance(json_message, str):
            if json_message == 'query_all_result':
                return self.batch_execute()
            else:
                raise ValueError("Incorrect request format")
        else:
            raise ValueError("Incorrect request format")

    def batch_execute(self):
        self.batch_result.clear()
        for name, command in self.command_dict.items():
            if command.check_status():
                result = command.execute()
                self.batch_result[command.get_name()] = result
        return self.batch_result

    def execute(self, command):
        return command.execute()