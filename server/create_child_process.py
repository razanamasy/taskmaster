import os
import signal
import sys
import copy
import struct
from contextlib import redirect_stdout, redirect_stderr
from timestamp import *
import resource

#retourner le tableau de PID au main server qui va wait dans la boucle principale
def main(data):
    pids = []
    stdout_original = sys.stdout
    stderr_original = sys.stderr
    stdout_fd = os.dup(stdout_original.fileno())
    stderr_fd = os.dup(stderr_original.fileno())
    data.stdout_fd = copy.deepcopy(stdout_fd)
    data.stderr_fd = copy.deepcopy(stderr_fd)
    data.stdout_og = copy.deepcopy(stdout_original.fileno())
    data.stderr_og = copy.deepcopy(stderr_original.fileno())
    for i in range(1):
        pid = os.fork()
        if pid == 0:
            # Child process
            try:
                
                stdout_file = open(data.stdout, "a")
                stderr_file = open(data.stderr, "a")

                os.dup2(stdout_file.fileno(), stdout_original.fileno())
                os.dup2(stderr_file.fileno(), stderr_original.fileno())

                try:
                    # Change the current working directory
                    if data.workingdir != None:
                        os.chdir(data.workingdir)

                    # Create a new dictionary for child process environment variables
                    child_env = os.environ.copy()

                    if data.env is not None:
                        for key, value in data.env.items():
                            child_env[key] = value
                
                    os.environ = child_env
                    command = data.cmd.split()
                    os.execve(command[0], command, os.environ)
                except Exception as e:
                    os.dup2(stdout_file.fileno(), stdout_original.fileno())
                    os.dup2(stderr_file.fileno(), stderr_original.fileno())
                    print(str(e) + "\n", end="", file=stderr_file)
                    if stdout_fd is not None:
                        os.dup2(stdout_fd, stdout_original.fileno())
                        os.close(stdout_fd)
                    if stderr_fd is not None:
                        os.dup2(stderr_fd, stderr_original.fileno())
                        os.close(stderr_fd)
                    sys.stdout = stdout_original
                    sys.stderr = stderr_original
                    print(timestamp('DEBG') + str(e) + "\n", file=sys.stdout, end="")
                    data.failure = (False, 0)
                    data.running = (False, 0)
                    data.backlog = (False, 0)
                    data.backoff_starting = (False, 0)
                    data.fatal = (False, 0)
                    data.quitting = (False, 0)
                    data.stopping = (False, 0)
                    data.stopped = (False, 0)
                    data.exited = (False, 0)
                    data.quit_with_stop = False
                    
                    sys.exit(1)  # Terminate child process with error status

            except Exception as e:
                print(timestamp('CRIT') + str(e) + "\n", flush=True, end="")
            # This line will never be reached
        else:
            pids.append(pid)

    return pid
