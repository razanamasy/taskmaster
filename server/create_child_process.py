import os
import signal
import sys
import logging
from contextlib import redirect_stdout, redirect_stderr

#retourner le tableau de PID au main server qui va wait dans la boucle principale
def main(data):

#    print("In create_child file proc data name is : ", data.name)
#    print("In create_child the cmd to execute is : ", data.cmd)
    logging.basicConfig(level=logging.DEBUG, filename="../Taskmasterd.logs", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")
    pids = []
    for i in range(1):
        pid = os.fork()
        if pid == 0:
            # Child process
            try:
                # Change the current working directory
                if data.workingdir != None:
                    try:
                        os.chdir(data.workingdir)
                    except Exception as e:
                        logging.debug(e)

                # Create a new dictionary for child process environment variables
                child_env = os.environ.copy()

                if data.env is not None:
                    for key, value in data.env.items():
                        child_env[key] = value
                
                os.environ = child_env
                
                stdout_original = sys.stdout
                stderr_original = sys.stderr
                stdout_fd = open(data.stdout, "a")
                stderr_fd = open(data.stderr, "a")
                os.dup2(stdout_fd.fileno(), sys.stdout.fileno())
                os.dup2(stderr_fd.fileno(), sys.stderr.fileno())

                os.execve(data.cmd, [data.name], os.environ)
            except Exception as e:
                os.close(stdout_fd.fileno())
                os.close(stderr_fd.fileno())
                os.dup2(stdout_original.fileno(), sys.stdout.fileno())
                os.dup2(stderr_original.fileno(), sys.stderr.fileno())
                logging.debug(e)
                os._exit(1)  # Terminate child process with error status
                # This line will never be reached
        else:
            pids.append(pid)

    return pid
