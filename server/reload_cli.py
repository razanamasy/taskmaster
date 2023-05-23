from start_launch import main as main_starting
from status_cli import main as status
from stop_cli import main as stop
import copy

def manage_process_key(new_process_key, old_process_key):
    to_reload = False
    if new_process_key.numprocs != old_process_key.numprocs:
        print("change")
        old_process_key.numprocs = new_process_key.numprocs
    if new_process_key.umask != old_process_key.umask:
        print("change")
        old_process_key.umask = new_process_key.umask
    if new_process_key.workingdir != old_process_key.workingdir:
        print("change")
        old_process_key.workingdir = new_process_key.workingdir
    if new_process_key.autostart != old_process_key.autostart:
        print("change")
        old_process_key.autostart = new_process_key.autostart
    if new_process_key.autorestart != old_process_key.autorestart:
        print("change")
        old_process_key.autorestart = new_process_key.autorestart
    if new_process_key.exitcodes != old_process_key.exitcodes:
        print("change")
        old_process_key.exitcode = new_process_key.exitcode
    if new_process_key.startretries != old_process_key.startretries:
        print("change")
        old_process_key.startretries = new_process_key.startretries
    if new_process_key.starttime != old_process_key.starttime:
        print("change")
        old_process_key.starttime = new_process_key.starttime
    if new_process_key.stopsignal != old_process_key.stopsignal:
        print("change")
        old_process_key.stopsignal = new_process_key.stopsignal
    if new_process_key.stoptime != old_process_key.stoptime:
        print("change")
        old_process_key.stoptime = new_process_key.stoptime
    if new_process_key.stdout != old_process_key.stdout:
        print("change")
        old_process_key.stdout = new_process_key.stdout
    if new_process_key.stderr != old_process_key.stderr:
        print("change")
        old_process_key.stderr = new_process_key.stderr
    if new_process_key.env != old_process_key.env:
        print("change")
        old_process_key.env = new_process_key.env
    if new_process_key.env != old_process_key.env:
        print("change")
        old_process_key.env = new_process_key.env


    if new_process_key.cmd != old_process_key.cmd:
        print("change need reload")
        old_process_key.cmd = new_process_key.cmd
        to_reload = True

    if to_reload:
        print("changes if reload")
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

    print(f"my new process after changes {old_process_key}")
    return to_reload

def main(new_list, list_proc_data, mutex_proc_dict, clients, running_table, thread_list):
    print(f"List process when calling reload {list_proc_data}")
    old_list = list_proc_data
    to_add = []

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
                print("need to reload stop it")
                stop(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)
                if list_proc_data[process_key].autostart == True:
                    print("If autostart, start it")
                    print(f"i'm restarting this shit because changes {process_key}")
                    main_starting(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)
                #RELOAD HERE
        else:
            to_add.append(process_key)

    for process_key in to_add:
        list_proc_data[process_key] = copy.deepcopy(new_list[process_key])
        if list_proc_data[process_key].autostart == True:
            print(f"i'm starting this shit because it did not exist ! {process_key}")
            main_starting(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)

    to_delete = []
    for process_key in old_list:
        if process_key not in new_list:
            to_delete.append(process_key)

    for process_key in to_delete:
        stop(list_proc_data, process_key, clients, running_table, mutex_proc_dict, thread_list)
        list_proc_data.pop(process_key)
