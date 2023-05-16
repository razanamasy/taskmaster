from start_launch import main as main_starting
#from server import is_exit_matching as is_exit_matching
import os
import signal

def is_exit_matching(status, process_data):
    exit_table = process_data.exitcodes
    match = 0
    for i in exit_table:
        print(f"compare {status} with {i}")
        if status == i:
            print("It has matched !!!")
            match = 1
    return match


def main(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list):
    process = client_proc_dict[fd][key]
    if process.backlog == True or process.running == True:
        print(f'Process {key} already running or backlog')
        return "Process " + key  + " already running or backlog"
    if process.autostart == False and process.pid == -1:
        process.cli_history.append('start')
        process.stopping = False
        process.stopped = False
        process.quit_with_stop = False
        main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
        return "Initial starting " + key
    else:
        if is_exit_matching(process.status_exit[-1], process) == 1 and process.fatal == False: #means it DID exit gracefully 
            print("Start work it exited gracefully")
            process.cli_history.append('start')
            process.stopping = False
            process.stopped = False
            process.quit_with_stop = False
            main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
            return "Starting " + key
        else:
            print("need to restart it didn't exit gracefully or is fatal")
            return "Need to restart process: " + key + ", because it didn't exit gracefully or is fatal"
