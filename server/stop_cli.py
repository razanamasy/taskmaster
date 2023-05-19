import copy
import os
import calendar
import time 
import signal
import threading
from create_child_process import main as main_exec
from threading import Thread, Lock

def timer(list_proc_data, key, curr_pid, running_table, mutex_proc_dict):
    process = list_proc_data[key]
    time.sleep(process.stoptime)
    print("end of sleep stop")
    if list_proc_data[key].pid == curr_pid: #Si pas eu d'autre start ou restart entre temp
        if list_proc_data[key].backlog[0] == True: #Clairement impossible lol
            return
        if list_proc_data[key].running[0] == False: #On a reussit a kill
            print("the process has stopped")
            return
        else:
            print("Stop failed Need to sigkill it")
            list_proc_data[key].quit_with_stop = True
            os.kill(process.pid, signal.SIGKILL)

def main(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    process = list_proc_data[key]
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.stopping[0] == True:
        print("Already in a stopping process")
        return "Process : " + key + " already in a stopping process"
    if process.backlog[0] == True:
        print("Already in a start process")
        return "Process : " + key + " already in a starting process"
    if process.running[0] == False:
        print("Already stopped")
        return "Process : " + key + " stopped"

    print(f"Really stopping {process.name}")
    process.cli_history.append('stop')
    process.stopping = (True, time_stamp)
    process.quit_with_stop = True
    stop_timer = threading.Thread(target=timer, args=(list_proc_data, key, copy.deepcopy(process.pid),running_table, mutex_proc_dict))

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
    return "Stopping process : " + key