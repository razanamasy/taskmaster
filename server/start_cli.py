from start_launch import main as main_starting
#from server import is_exit_matching as is_exit_matching
import os
import signal
import calendar
import time
from timestamp import *

def is_exit_matching(status, process_data):
    exit_table = process_data.exitcodes
    match = 0
    for i in exit_table:
        if status == i:
            match = 1
    return match


def main(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    process = list_proc_data[key]
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.backlog[0] == True or process.running[0] == True:
        print(timestamp('WARN') + "Process " + key  + " already running or backlog", flush=True)
        return "Process " + key  + " already running or backlog"
    if process.autostart == False and process.pid == -1:
        process.cli_history.append('start')
        process.stopping = (False, time_stamp)
        process.stopped = (False, time_stamp)
        process.quit_with_stop = False
        main_starting(list_roc_data, key, clients, running_table, mutex_proc_dict, thread_list)
        print(timestamp('INFO') + "Initial starting " + key, flush=True)
        return "Initial starting " + key
    else:
        if is_exit_matching(process.status_exit[-1], process) == 1 and process.fatal[0] == False: #means it DID exit gracefully
            print(timestamp('INFO') + "Starting " + key, flush=True)
            res = "Starting " + key
        else:
            print(timestamp('INFO') + "Starting : " + key + " (didn't exit with an uxpected exit code or was fatal)", flush=True)
            res = "Starting : " + key + " (didn't exit with an uxpected exit code or was fatal)"
        process.cli_history.append('start')
        process.stopping = (False, time_stamp)
        process.stopped = (False, time_stamp)
        process.quit_with_stop = False
        main_starting(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
        return res

