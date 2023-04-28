import os
import signal

# Start an undefined number of child processes

env = {"USER": "hrazanam", "HOME": "/home/hrazanam"}

pids = []
for i in range(5):
    pid = os.fork()
    if pid == 0:
        # Child process
		#Ici ajout du PID a sa class process correspondante
        os.execve("/home/hrazanam/taskmaster/progs/while", ['while'], env)
        # This line will never be reached
    else:
			#     os.kill(pid, signal.SIGKILL)
        pids.append(pid)

# Wait for all child processes to exit
while pids:
    pid, status = os.waitpid(-1, 0)
    print(f"Process {pid} exited with status {status}")
 #   pids.remove(pid)
