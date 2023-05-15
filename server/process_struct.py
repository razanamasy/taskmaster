class process_data:
    def __init__(self, name):
        self.name = name
        self.client = None
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
        self.failure = False
        self.running = False
        self.backlog = False
        self.fatal = False
        self.quitting = False
        self.stopping = False
        self.logs = []
        self.cli_history = []
        self.status_exit = []

    def __str__(self):
        return f"My class: \n name = {self.name}\n client = {self.client}\n pid = {self.pid}\n cmd = {self.cmd}\n numprocs = {self.numprocs}\n \
umask = {self.umask}\n workingdir = {self.workingdir}\n autostart = {self.autostart}\n \
autorestart = {self.autorestart}\n exitcodes = {self.exitcodes}\n startretries = {self.startretries}\n \
starttime = {self.starttime}\n stopsignal = {self.stopsignal}\n stoptime = {self.stoptime}\n \
stdout = {self.stdout}\n stderr = {self.stderr}\n env = {self.env}\n failure = {self.failure}\n \
running = {self.running}\n backlog= {self.backlog}\n fatal = {self.fatal}\n logs = {self.logs}\n"
