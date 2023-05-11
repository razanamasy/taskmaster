import time
import threading
import copy
from create_child_process import main as main_exec
from threading import Thread, Lock

def starting_process(client_proc_dict, fd, key, running_table, mutex_proc_dict):
    client_proc_dict[fd][key].running = False #A delete car deja fait dans le monitor
    my_retries = copy.deepcopy(client_proc_dict[fd][key].startretries)
    while my_retries and (client_proc_dict[fd][key].running == False):
        print("MY RETRIES = ", my_retries)
        mutex_proc_dict.acquire()
        my_retries -= 1
        mutex_proc_dict.release()
        time.sleep(client_proc_dict[fd][key].starttime)
        if fd in client_proc_dict:
            if client_proc_dict[fd][key].pid in running_table:
                client_proc_dict[fd][key].running = True
                client_proc_dict[fd][key].failure = False
                client_proc_dict[fd][key].backlog = False
                print("end of story for start pass to reload for : ", client_proc_dict[fd][key].name)
            else: #Fork
                print("Pid not in running table, neet to retry for :", client_proc_dict[fd][key].name)
                client_proc_dict[fd][key].backlog = True
                client_proc_dict[fd][key].failure = True
                if my_retries == 0:
                    client_proc_dict[fd][key].fatal = True
                newpid = main_exec(client_proc_dict[fd][key])
                client_proc_dict[fd][key].pid = newpid
                running_table[newpid]=client_proc_dict[fd][key]
        else:
            break

    if fd in client_proc_dict:
        mutex_proc_dict.acquire()
        print("NUMER RETRIES LEFT END OF WHILE", client_proc_dict[fd][key].startretries, "Failure is : ", client_proc_dict[fd][key].failure)
        if client_proc_dict[fd][key].startretries == 0 and client_proc_dict[fd][key].failure == True:
            client_proc_dict[fd][key].fatal = True
            client_proc_dict[fd][key].backlog = False
        print("FINAL START PROCESS FOR --->i", client_proc_dict[fd][key].name," Fatal:", client_proc_dict[fd][key].fatal, " Running:", client_proc_dict[fd][key].running, " Failure:", client_proc_dict[fd][key].failure )
        mutex_proc_dict.release()

def main (client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list):
    print("MAIN STARTING CALLED")
    #Fork premiere execution
    newpid = main_exec(client_proc_dict[fd][key])

    client_proc_dict[fd][key].pid = newpid
    client_proc_dict[fd][key].backlog = True
    running_table[newpid]=client_proc_dict[fd][key]

    #envoi du thread starting process pour chaque process
    thread_starting_process = threading.Thread(target=starting_process, args=(client_proc_dict, fd, key, running_table, mutex_proc_dict))
 #   thread_starting_process.daemon = True
    thread_list.append(thread_starting_process)
    thread_starting_process.start()

