import os
import signal
import sys
import copy
from contextlib import redirect_stdout, redirect_stderr

#retourner le tableau de PID au main server qui va wait dans la boucle principale
def main(data):

#    print("In create_child file proc data name is : ", data.name)
#    print("In create_child the cmd to execute is : ", data.cmd)
    pids = []
 #   stdout_original = sys.stdout
 #   stderr_original = sys.stderr
 #   stdout_fd = os.dup(stdout_original.fileno())
 #   stderr_fd = os.dup(stderr_original.fileno())
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
                        print(e)

                # Create a new dictionary for child process environment variables
                child_env = os.environ.copy()

                if data.env is not None:
                    for key, value in data.env.items():
                        child_env[key] = value
                
                os.environ = child_env
                
           #     stdout_file = open(data.stdout, "a")
           #     stderr_file = open(data.stderr, "a")
           #     os.dup2(stdout_file.fileno(), stdout_original.fileno())
           #     os.dup2(stderr_file.fileno(), stderr_original.fileno())

                command = data.cmd.split()
                os.execve(command[0], command, os.environ)
            except Exception as e:
          #      os.dup2(stdout_file.fileno(), stdout_original.fileno())
          #      os.dup2(stderr_file.fileno(), stderr_original.fileno())
          #      print(str(e), file=stderr_file)
          #      if stdout_fd is not None:
          #          os.dup2(stdout_fd, stdout_original.fileno())
          #          os.close(stdout_fd)
          ##      if stderr_fd is not None:
          #          os.dup2(stderr_fd, stderr_original.fileno())
          #          os.close(stderr_fd)
          #      sys.stdout = stdout_original
          #      sys.stderr = stderr_original
          #      print(str(e), file=sys.stdout)
                
                sys.exit(1)  # Terminate child process with error status
                # This line will never be reached
        else:
            pids.append(pid)

    return pid
