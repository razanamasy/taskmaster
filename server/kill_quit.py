import os
import signal
from threading import Thread, Lock

def main(list_proc_data, running_table, mutex_proc_dict):
     
    #client_proc_dict
    print("kill all pid (last client)", flush=True)
    for key in list_proc_data:
        print(f"process to kill : {list_proc_data.keys()} ", flush=True )    
        list_proc_data[key].quitting = True
        try:
            os.kill(list_proc_data[key].pid, signal.SIGKILL)
        except ProcessLookupError:
            print(f"Process with PID {list_proc_data[key].pid} does not exist.", flush=True)
