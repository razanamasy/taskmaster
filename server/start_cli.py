from start_launch import main as main_starting
#from server import is_exit_matching as is_exit_matching
import os
import signal
import calendar
import time
from timestamp import *

def main(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    process = list_proc_data[key]
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.backlog[0] == True or process.running[0] == True or process.stopping[0] == True:
        print(timestamp('WARN') + "Process " + key  + " already running stopping process or starting process\n", end="", flush=True)
        return "Process " + key  + " already running stopping process or starting process"
    if process.autostart == False and process.pid == -1:
        process.cli_history.append('start')
        process.stopping = (False, time_stamp)
        process.stopped = (False, time_stamp)
        process.fatal = (False, time_stamp)
        process.quit_with_stop = False
        main_starting(list_roc_data, key, clients, running_table, mutex_proc_dict, thread_list)
        print(timestamp('INFO') + "Initial starting " + key + "\n", end="", flush=True)
        return "Initial starting " + key
    else:
        print(timestamp('INFO') + "Starting : " + key + "\n", end="", flush=True)
        res = "Starting : " + key
        process.cli_history.append('start')
        process.stopping = (False, time_stamp)
        process.stopped = (False, time_stamp)
        process.fatal = (False, time_stamp)
        process.quit_with_stop = False
        main_starting(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
        return res

