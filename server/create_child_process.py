import os
import signal

def main():
    env = {"USER": "hrazanam", "HOME": "/home/hrazanam"}

    pids = []
    for i in range(5):
        pid = os.fork()
        if pid == 0:
            # Child process
            os.execve("/Users/hinaraza/42/cursus/taskmaster/progs/while", ['while'], env)
            # This line will never be reached
        else:
            pids.append(pid)

    # Wait for all child processes to exit
#    while pids:
#        pid, status = os.waitpid(-1, 0)
#        print(f"Process {pid} exited with status {status}")

if __name__ == '__main__':
    main()
