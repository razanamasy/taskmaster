import os
import signal
import sys


#retourner le tableau de PID au main server qui va wait dans la boucle principale
def main(data):
    env = {"USER": "hrazanam", "HOME": "/home/hrazanam"}

#    print("In create_child file proc data name is : ", data.name)
#    print("In create_child the cmd to execute is : ", data.cmd)

    pids = []
    for i in range(1):
        pid = os.fork()
        if pid == 0:
            # Child process
            os.execve(data.cmd, [data.name], env)
            # This line will never be reached
        else:
            pids.append(pid)

    return pid
