
__all__ = ('HostReceiver', 'JobReceiver', 'LoadReceiver', \
           'QueueReceiver', 'UserReceiver','ShellReceiver',)

class ShellReceiver():
    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.shell_info = None

    def get_shell_stream(self, command=None):
        if self._exec_func:
            self.shell_info = self._exec_func(command)

        return self.shell_info

class HostReceiver():

    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.host_info = None

    def get_bhost_stream(self, command=None):
        """
        Get lshosts info with command 'lshosts'.
        ====
        HOST_NAME      type    model  cpuf ncpus maxmem maxswp server RESOURCES
        lavaHost1     linux  IntelI5 100.0     2  7807M  5119M    Yes (cs)
        ====
        """
        if self._exec_func:
            self.host_info = self._exec_func(command)

        return self.host_info

    def get_lshost_stream(self, command=None):
        """
        Get lsload info with command 'lsload'.
        ====
        HOST_NAME       status  r15s   r1m  r15m   ut    pg  ls    it   tmp   swp   mem
        lavaHost1           ok   0.3   0.1   0.1  19%   0.0   3     5   35G 5120M 6688M
        ====
        """
        if self._exec_func:
            self.host_info = self._exec_func(command)

        return self.host_info

class JobReceiver():

    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.job_info = None

    def get_bjobs_stream(self, command=None):
        """
        Get bjobs info with command 'bjobs'.
        ====
        JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
        146940  tao.che RUN   short      etxnode02   cm067       abstract   Aug  2 21:00  
        ====
        """
        if self._exec_func:
            self.job_info = self._exec_func(command)
        
        return self.job_info
    
class LoadReceiver():
    
    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.load_info = None

    def get_lsloads_stream(self, command=None):
        """
        Get lsload info with command 'lsload'.
        ====
        HOST_NAME       status  r15s   r1m  r15m   ut    pg  ls    it   tmp   swp   mem
        lavaHost1           ok   0.3   0.1   0.1  19%   0.0   3     5   35G 5120M 6688M
        ====
        """
        if self._exec_func:
            self.load_info = self._exec_func(command)

        return self.load_info

class QueueReceiver():
    
    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.queue_info = None

    def get_bqueues_stream(self, command=None):
        """
        Get bqueues info with command 'bqueues'.
        ====
        QUEUE_NAME     PRIO      STATUS      MAX  JL/U JL/P JL/H NJOBS  PEND  RUN  SUSP
        normal          30    Open:Active      -    -    -    -     1     0     1     0
        ====
        """
        if self._exec_func:
            self.queue_info = self._exec_func(command)

        return self.queue_info

class UserReceiver():
    
    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.user_info = None

    def get_busers_stream(self, command=None):
        """
        Get lsload info with command 'busers'.
        ====
        USER/GROUP          JL/P    MAX  NJOBS   PEND    RUN  SSUSP  USUSP    RSV 
        yanqing.li             -      -      0      0      0      0      0      0
        ====
        """
        if self._exec_func:
            self.user_info = self._exec_func(command)
        
        return self.user_info

class ClusterReceiver():

    def __init__(self, exec_func=None):
        self._exec_func = exec_func
        self.cluster_info = None
    
    def get_lscluster_stream(self, command=None):
        if self._exec_func:
            self.cluster_info = self._exec_func(command)
        
        return self.cluster_info