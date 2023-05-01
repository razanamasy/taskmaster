<<<<<<< HEAD
class process:
=======
class process_data:
>>>>>>> master
    def __init__(self, name):
        self.name = name
        self.cmd = ""
        self.numprocs = 1
        self.umask = "022"
        self.workingdir = ""
        self.autostart = True
        self.autorestart = "unexpected"
        self.exitcode = [0]
        self.startretries = 3
        self.starttime = 1
        self.stopsignal = "TERM"
        self.stoptime = 10
        self.stdout = "/etc/taskmaster/stdout/" + name
        self.stderr = "/etc/taskmaster/stderr/" + name
        self.env = []
        self.failure = False
        self.fatal = False
        self.logs = []

    def __str__(self):
        return f"My class: \n name = {self.name}\n cmd = {self.cmd}\n numprocs = {self.numprocs}\n \
umask = {self.umask}\n workingdir = {self.workingdir}\n autostart = {self.autostart}\n \
autorestart = {self.autorestart}\n exitcode = {self.exitcode}\n startretries = {self.startretries}\n \
starttime = {self.starttime}\n stopsignal = {self.starttime}\n stoptime = {self.stoptime}\n \
stdout = {self.stdout}\n stderr = {self.stderr}\n env = {self.env}\n failure = {self.failure}\n \
fatal = {self.fatal}\n logs = {self.logs}\n"
<<<<<<< HEAD

=======
>>>>>>> master
