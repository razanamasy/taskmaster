import os
import signal
from threading import Thread, Lock

def main(client_fd, client_proc_dict, running_table):
     
    #client_proc_dict
    print("Killin pid of this quitting client : ", client_fd)
    for sub_value in client_proc_dict[client_fd]:
     #   print("Name of pid we will try to kill : ", client_proc_dict[client_fd][sub_value].name)
     #   print("IT's PID : ", client_proc_dict[client_fd][sub_value].pid)
        #First pop from running table then try to kill
        print("I've juste popped the pid from running table")
        if client_fd in client_proc_dict:
            client_proc_dict[client_fd][sub_value].quitting = True
        try:
            if (client_proc_dict[client_fd][sub_value].fatal == False):
                os.kill(client_proc_dict[client_fd][sub_value].pid, signal.SIGTERM)
                print(f"Process with PID {client_proc_dict[client_fd][sub_value].pid} exists. We can kill it")
            else:
                print("This shit is fatal")
        except ProcessLookupError:
            print(f"Process with PID {client_proc_dict[client_fd][sub_value].pid} does not exist.")
