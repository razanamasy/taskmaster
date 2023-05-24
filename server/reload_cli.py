from start_launch import main as main_starting
from status_cli import main as status
from stop_cli import main as stop
import calendar
import time
import copy

def manage_process_key(new_process_key, old_process_key):
    to_reload = False
    if new_process_key.numprocs != old_process_key.numprocs:
        print(f"change replicas for : {new_process_key.name}", flush=True)
        old_process_key.numprocs = new_process_key.numprocs
    if new_process_key.umask != old_process_key.umask:
        print("change umask for : {new_process_key.name}", flush=True)
        old_process_key.umask = new_process_key.umask
    if new_process_key.workingdir != old_process_key.workingdir:
        print("change workingdir for : {new_process_key.name}", flush=True)
        old_process_key.workingdir = new_process_key.workingdir
    if new_process_key.autostart != old_process_key.autostart:
        print("change autostart for : {new_process_key.name}", flush=True)
        old_process_key.autostart = new_process_key.autostart
    if new_process_key.autorestart != old_process_key.autorestart:
        print("change autorestart for : {new_process_key.name}", flush=True)
        old_process_key.autorestart = new_process_key.autorestart
    if new_process_key.exitcodes != old_process_key.exitcodes:
        print("change exitcodes for : {new_process_key.name}", flush=True)
        old_process_key.exitcode = new_process_key.exitcode
    if new_process_key.startretries != old_process_key.startretries:
        print("change startretries for : {new_process_key.name}", flush=True)
        old_process_key.startretries = new_process_key.startretries
    if new_process_key.starttime != old_process_key.starttime:
        print("change starttime for : {new_process_key.name}", flush=True)
        old_process_key.starttime = new_process_key.starttime
    if new_process_key.stopsignal != old_process_key.stopsignal:
        print("change stopsignal for : {new_process_key.name}", flush=True)
        old_process_key.stopsignal = new_process_key.stopsignal
    if new_process_key.stoptime != old_process_key.stoptime:
        print("change stoptime for : {new_process_key.name}", flush=True)
        old_process_key.stoptime = new_process_key.stoptime
    if new_process_key.stdout != old_process_key.stdout:
        print("change stdout for : {new_process_key.name}", flush=True)
        old_process_key.stdout = new_process_key.stdout
    if new_process_key.stderr != old_process_key.stderr:
        print("change stderr for : {new_process_key.name}", flush=True)
        old_process_key.stderr = new_process_key.stderr
    if new_process_key.env != old_process_key.env:
        print("change env for : {new_process_key.name}", flush=True)
        old_process_key.env = new_process_key.env


    if new_process_key.cmd != old_process_key.cmd:
        print("This process need to be restarted because command changed : {new_process_key.name}", flush=True)
        old_process_key.cmd = new_process_key.cmd
        to_reload = True

    if to_reload:
        if new_process_key.running != old_process_key.running:
            old_process_key.running = new_process_key.running
        if new_process_key.backlog != old_process_key.backlog:
            old_process_key.backlog = new_process_key.backlog
        if new_process_key.backoff_starting != old_process_key.backoff_starting:
            old_process_key.backoff_starting = new_process_key.backoff_starting
        if new_process_key.fatal != old_process_key.fatal:
            old_process_key.fatal = new_process_key.fatal
        if new_process_key.quitting != old_process_key.quitting:
            old_process_key.quitting = new_process_key.quitting
        if new_process_key.stopping != old_process_key.stopping:
            old_process_key.stopping = new_process_key.stopping
        if new_process_key.stopped != old_process_key.stopped:
            old_process_key.stopped = new_process_key.stopped
        if new_process_key.exited != old_process_key.exited:
            old_process_key.exited = new_process_key.exited
        if new_process_key.quit_with_stop != old_process_key.quit_with_stop:
            old_process_key.quit_with_stop = new_process_key.quit_with_stop

    return to_reload

def main(new_list, list_proc_data, mutex_proc_dict, clients, running_table, thread_list):
    old_list = list_proc_data
    to_add = []

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    #First add the replicas to the new list 
    temp_dico = {}
    for key in new_list:
        print(key)
        if new_list[key].numprocs > 1:
            i = 1
            while i < new_list[key].numprocs:
                temp_dico[key + "-" + str(i)] = copy.deepcopy(new_list[key])
                temp_dico[key + "-" + str(i)].name = key + "-" + str(i)
                temp_dico[key + "-" + str(i)].numprocs = 1
                i += 1
    #UPDATE PROCES TO RUN
    new_list.update(temp_dico)


    #check the changes in new list
    for process_key in new_list:
        if process_key in old_list:
            if manage_process_key(new_list[process_key], old_list[process_key]) == True:
                stop(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)
                if list_proc_data[process_key].autostart == True:
                    list_proc_data[process_key].cli_history.append('start')
                    list_proc_data[process_key].stopping = (False, time_stamp)
                    list_proc_data[process_key].stopped = (False, time_stamp)
                    list_proc_data[process_key].quit_with_stop = False
                    main_starting(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)
                #RELOAD HERE
        else:
            to_add.append(process_key)

    for process_key in to_add:
        list_proc_data[process_key] = copy.deepcopy(new_list[process_key])
        if list_proc_data[process_key].autostart == True:
            print(f"Add process : {process_key}", flush=True)
            main_starting(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)

    to_delete = []
    for process_key in old_list:
        if process_key not in new_list:
            to_delete.append(process_key)

    for process_key in to_delete:
        print(f"Delete process : {process_key}", flush=True)
        stop(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)
        list_proc_data.pop(process_key)
