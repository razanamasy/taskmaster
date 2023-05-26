class process_data:
    def __init__(self, name):
        self.name = name
        self.pid = -1
        self.cmd = None
        self.numprocs = 1
        self.umask = "022"
        self.workingdir = None
        self.autostart = True
        self.autorestart = "unexpected"
        self.exitcodes = [0]
        self.startretries = 3
        self.starttime = 1
        self.stopsignal = "SIGTERM"
        self.stoptime = 10
        self.stdout = "/etc/taskmaster/stdout/" + name
        self.stderr = "/etc/taskmaster/stderr/" + name
        self.env = None
        self.failure = (False, 0) #real state useless 
        self.running = (False, 0) #Real state
        self.backlog = (False, 0) # Real state
        self.backoff_starting = (False, 0) # Real state True == starting False == backoff
        self.fatal = (False, 0) # Real state
        self.quitting = False #utils flag
        self.stopping = (False, 0) #A real state in process stopping AND used as flag to avoid multiple stop call
        self.stopped = (False, 0) #A real state all process detected by wait need it
        self.exited = (False, 0) #A real state all process detected by wait need it
        self.quit_with_stop = False #a utils flag to avoid autorestart
        self.logs = []
        self.cli_history = []
        self.status_exit = []
        self.obsolete_pid = []
        self.stdout_fd = -1
        self.stderr_fd = -1
        self.stdout_og = -1
        self.stderr_og = -1 

    def __str__(self):
        return f"My class: \n name = {self.name}\n pid = {self.pid}\n cmd = {self.cmd}\n numprocs = {self.numprocs}\n \
umask = {self.umask}\n workingdir = {self.workingdir}\n autostart = {self.autostart}\n \
autorestart = {self.autorestart}\n exitcodes = {self.exitcodes}\n startretries = {self.startretries}\n \
starttime = {self.starttime}\n stopsignal = {self.stopsignal}\n stoptime = {self.stoptime}\n \
stdout = {self.stdout}\n stderr = {self.stderr}\n env = {self.env}\n failure = {self.failure}\n \
running = {self.running}\n backlog = {self.backlog}\n fatal = {self.fatal}\n \
quitting = {self.quitting}\n stopping = {self.stopping}\n stopped = {self.stopped}\n \
quit_with_stop = {self.quit_with_stop}\n logs = {self.logs}\n \
status_exit = {self.status_exit}\n logs = {self.logs}\n cli_history = {self.cli_history}\n"
