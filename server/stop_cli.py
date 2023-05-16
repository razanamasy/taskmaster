import copy
import os
import time 
import signal
import threading
from create_child_process import main as main_exec
from threading import Thread, Lock

def timer(client_proc_dict, fd, key, curr_pid, running_table, mutex_proc_dict):
    process = client_proc_dict[fd][key]
    time.sleep(process.stoptime)
    print("end of sleep stop")
    if process.pid == curr_pid: #Si pas eu d'autre start ou restart entre temp
        if process.backlog == True: #Clairement impossible lol
            return
        if process.running == False: #On a reussit a kill
            print("the process has stopped")
            return
        else:
            print("Stop failed Need to sigkill it")
            process.quit_with_stop = True
            os.kill(process.pid, signal.SIGKILL)

def main(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list):
    
    process = client_proc_dict[fd][key]
    if process.stopping == True:
        print("Already in a start process")
        return
    if process.backlog == True:
        print("Already in a start process")
        return
    if process.running == False:
        print("Already stopped")
        return

    print(f"Really stopping {process.name}")
    process.cli_history.append('stop')
    process.stopping = True
    process.quit_with_stop = True
    stop_timer = threading.Thread(target=timer, args=(client_proc_dict, fd, key, copy.deepcopy(process.pid),running_table, mutex_proc_dict))

    if process.stopsignal == "TERM":
        print("STOP WITH SIGTERM")
        os.kill(process.pid, signal.SIGTERM)
    elif process.stopsignal == "HUP":
        os.kill(process.pid, signal.SIGHUP)
    elif process.stopsignal == "INT":
        os.kill(process.pid, signal.SIGINT)
    elif process.stopsignal == "QUIT":
        os.kill(process.pid, signal.SIGQUIT)
    elif process.stopsignal == "KILL":
        print("STOP WITH SIGTERM")
        os.kill(process.pid, signal.SIGKILL)
    elif process.stopsignal == "USR1":
        os.kill(process.pid, signal.SIGUSR1)
    elif process.stopsignal == "USR2":
        os.kill(process.pid, signal.SIGUSR2)
    thread_list.append(stop_timer)
    stop_timer.start()
