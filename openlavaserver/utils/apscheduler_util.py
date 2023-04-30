
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

__all__ = ('TimeScheduler',)

# 存储方式配置
jobstores = {
    'default': MemoryJobStore(),
}

# 执行器配置
executors = {
    'default': ThreadPoolExecutor(20),
}


job_defaults = {
    # 设置 coalesce为 True：设置这个目的是
    # 比如由于某个原因导致某个任务积攒了很多次没有执行（比如有一个任务是1分钟跑一次，但是系统原因断了5分钟）
    # 如果 coalesce=True，那么下次恢复运行的时候，会只执行一次
    # 而如果设置 coalesce=False，那么就不会合并，会5次全部执行。
    'coalesce': True,
    # 同一个任务同一时间最多只能有5个实例在运行
    'max_instances': 30
}

class TriggerModule:

    def __init__(self, trigger=None, param=None):
        if not trigger or not param:
            raise ValueError("TriggerModule init error")
        self.trigger = trigger
        self.param = param
    
    def get_trigger(self):
        return self.trigger

    def get_param(self):
        return self.param
    

class TimeScheduler:

    def __init__(self):
        # 调度器设置
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        self.job_info = {}
        self.params = {"trigger": "interval", "minutes": 1}

    #需要进行重构
    def add_job(self, job_id=None, job_name=None):
        if not job_id or not job_name:
            raise ValueError("TimeScheduler add job error")
            
        if job_id not in self.job_info:
            job = self.scheduler.add_job(id=job_id, func=job_name, **self.params)
            if job_id in self.job_info:
                raise ValueError("Job id repeated")
            self.job_info[job_id] = job

    def add_listener(self, listerner):
        if not listerner:
            raise ValueError("Listener is None")
        self.scheduler.add_listener(listerner, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def remove_job(self, job_id):
        if job_id not in self.job_info:
            raise ValueError("Job id is not exist, remove error")    
        self.scheduler.remove_job(job_id)
    
    def modify_job(self, job_id, jobstore=None, **changes):
        if job_id not in self.job_info:
            raise ValueError("Job id is not exist, remove error")  
        
        self.scheduler.modify_job(job_id, jobstore, changes)
        
    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

        

