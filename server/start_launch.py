import time
import threading
from create_child_process import main as main_exec

def starting_time(start_time, pid, running_table)
    time.sleep(start_time);

def main(client_proc_dict, fd, key, running_table):
	#Fork execution
    newpid = main_exec(client_proc_dict[fd][key]);
    client_proc_dict[fd][key].pid = newpid;
    running_table[newpid]=client_proc_dict[fd][key];

	#Thread wich will sleep
 #   threading.Thread(target=starting_time(client_proc_dict[fd][key].starttime, pid, running_table))
