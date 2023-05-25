import os
import signal
from threading import Thread, Lock
from timestamp import *

def main(list_proc_data, running_table, mutex_proc_dict):
     
    #client_proc_dict
    print(timestamp('INFO') + "kill all pid (last client)\n", end="", flush=True)
    for key in list_proc_data:    
        list_proc_data[key].quitting = True
        try:
            os.kill(list_proc_data[key].pid, signal.SIGKILL)
        except ProcessLookupError:
            print(timestamp('WARN') + f"Process with PID {list_proc_data[key].pid} does not exist.\n", end="", flush=True)
