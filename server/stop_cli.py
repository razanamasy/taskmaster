import copy
import os
import calendar
import time 
import signal
import threading
from threading import Thread, Lock
from timestamp import *

def timer(list_proc_data, key, curr_pid, running_table, mutex_proc_dict):
    process = list_proc_data[key]
    time.sleep(process.stoptime)
    print(timestamp('INFO') + "end of stoptime\n", end="", flush=True)
    if key not in list_proc_data:
        return
    if list_proc_data[key].pid == curr_pid: #Si pas eu d'autre start ou restart entre temp
        if list_proc_data[key].backlog[0] == True: #Clairement impossible lol
            return
        if list_proc_data[key].running[0] == False: #On a reussit a kill
            print(timestamp('WARN') + "the process has already stopped\n", end="", flush=True)
            return
        else:
            print(timestamp('WARN') + "Stop failed Need to sigkill it\n", end="", flush=True)
            list_proc_data[key].quit_with_stop = True
            os.kill(process.pid, signal.SIGKILL)

def main(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    print(timestamp('INFO') + f"THIS PROCESS ENTER IN STOP {key}\n", end="", flush=True)
    process = list_proc_data[key]
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    process.backlog = (False, time_stamp)
    process.quit_with_stop = True
    process.obsolete_pid.append(process.pid)

    if process.stopping[0] == True:
        print(timestamp('WARN') + "Process : " + key + " already in a stopping process\n", end="", flush=True)
        return "Process : " + key + " already in a stopping process"
    if process.backlog[0] == True and process.backoff_starting[0] == False: #en backoff
        process.quit_with_stop = True
        process.stopped = (True, time_stamp)
        process.obsolete_pid.append(process.pid)
        print(timestamp('INFO') + "Old state of :" + key + " BACKOFF, stopping the start process\n", end="", flush=True)
        return "Old state of :" + key + " BACKOFF, stopping the start process"
#        return "Process : " + key + " already in a starting process"

    if process.exited[0] == True:
        process.stopped = (True, time_stamp) #in case of exited ls to fast
        print(timestamp('WARN') + "Already exited Process : " + key + " now stopped\n", end="", flush=True)
        return "Already exited Process : " + key + " now stopped"
    if process.stopped[0] == True or process.fatal[0] == True:
        print(timestamp('WARN') + "Already stopped Process : " + key + " stopped" + " or fatal : " + str(process.exited[0]) + " and " +  str(process.fatal[0]) + "\n", end="", flush=True)
        return "Already stopped Process : " + key + " stopped" + " or fatal : " + str(process.exited[0]) + " and " +  str(process.fatal[0])

    process.cli_history.append('stop')
    process.stopping = (True, time_stamp)
    process.quit_with_stop = True
    stop_timer = threading.Thread(target=timer, args=(list_proc_data, key, copy.deepcopy(process.pid),running_table, mutex_proc_dict))

    try:
        if process.stopsignal == "TERM":
            os.kill(process.pid, signal.SIGTERM)
        elif process.stopsignal == "HUP":
            os.kill(process.pid, signal.SIGHUP)
        elif process.stopsignal == "INT":
            os.kill(process.pid, signal.SIGINT)
        elif process.stopsignal == "QUIT":
            os.kill(process.pid, signal.SIGQUIT)
        elif process.stopsignal == "KILL":
            os.kill(process.pid, signal.SIGKILL)
        elif process.stopsignal == "USR1":
            os.kill(process.pid, signal.SIGUSR1)
        elif process.stopsignal == "USR2":
            os.kill(process.pid, signal.SIGUSR2)
        thread_list.append(stop_timer)
        stop_timer.start()
        print(timestamp('INFO') + "Stopping process : " + key + "\n", end="", flush=True)
        return "Stopping process : " + key
    except OSError as e:
        print(timestamp('ERRO') +  "key :" + str(e) + "\n", end="", flush=True)
        return "key :" + str(e)
