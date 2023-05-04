import time
import threading
from create_child_process import main as main_exec

def starting_process(client_proc_dict, fd, key, running_table):
    while client_proc_dict[fd][key].startretries and client_proc_dict[fd][key].starttime:
        print("my starting time for", client_proc_dict[fd][key].name,"is : ", client_proc_dict[fd][key].starttime)
        time.sleep(client_proc_dict[fd][key].starttime);
        print("end sleeping")
        if client_proc_dict[fd][key].pid in running_table:
            client_proc_dict[fd][key].starttime = 0
            client_proc_dict[fd][key].running = True
            client_proc_dict[fd][key].failure = False
            print("end of story for start pass to reload for : ", client_proc_dict[fd][key].name)
        else: #Fork
            print("Pid not in running table, neet to retry for :", client_proc_dict[fd][key].name)
            client_proc_dict[fd][key].backlog = True
            client_proc_dict[fd][key].failure = True
            newpid = main_exec(client_proc_dict[fd][key]);
            client_proc_dict[fd][key].pid = newpid;
            running_table[newpid]=client_proc_dict[fd][key]; 
            client_proc_dict[fd][key].startretries -= 1

    if client_proc_dict[fd][key].failure == True:
        client_proc_dict[fd][key].fatal = True
    client_proc_dict[fd][key].backlog = False
    print("FINAL START PROCESS FOR --->i", client_proc_dict[fd][key].name," Fatal:", client_proc_dict[fd][key].fatal, " Running:", client_proc_dict[fd][key].running, " Failure:", client_proc_dict[fd][key].failure )

def main (client_proc_dict, fd, key, running_table):
	#Fork premiere execution
    newpid = main_exec(client_proc_dict[fd][key]);
    client_proc_dict[fd][key].pid = newpid;
    running_table[newpid]=client_proc_dict[fd][key];

	#envoi du thread starting process pour chaque process
    thread_starting_process = threading.Thread(target=starting_process, args=(client_proc_dict, fd, key, running_table))
    thread_starting_process.daemon = True
    thread_starting_process.start()

