import calendar
import time
import threading
import copy
from create_child_process import main as main_exec
from threading import Thread, Lock

def starting_process(list_proc_data, key, clients, running_table, mutex_proc_dict):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    my_retries = copy.deepcopy(list_proc_data[key].startretries)

    mutex_proc_dict.acquire()
    last_starting = list_proc_data[key].backoff_starting[1] 
    mutex_proc_dict.release()
    while time_stamp - last_starting <= list_proc_data[key].starttime:
        if len(clients) != 0: #Check also if has not been stopped to avoid revival process

            mutex_proc_dict.acquire()
            if list_proc_data[key].fatal[0] == True:
                break
            mutex_proc_dict.release()
            if list_proc_data[key].pid not in running_table:
                print("Pid not in process_table, need to retry for :", list_proc_data[key].name)
                if my_retries == 0:
                    print("But no retries left it's fataal:", list_proc_data[key].name)
                    list_proc_data[key].fatal = (True, time_stamp)
                    break

                mutex_proc_dict.acquire()
                list_proc_data[key].backoff_starting = (False, time_stamp) 
                mutex_proc_dict.release()
                time.sleep(list_proc_data[key].startretries - my_retries)
                mutex_proc_dict.acquire()
                last_starting = list_proc_data[key].backoff_starting[1] 
                mutex_proc_dict.release()

                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)

                mutex_proc_dict.acquire()
                list_proc_data[key].backoff_starting = (True, time_stamp) #reset startsecs from last starting (substraction ts - b_s.ts)
                mutex_proc_dict.release()
                newpid = main_exec(list_proc_data[key])
                my_retries -= 1
                list_proc_data[key].pid = newpid
                running_table[newpid]=list_proc_data[key]
        else:
            break
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

    if len(clients) != 0:
        mutex_proc_dict.acquire()
        list_proc_data[key].backlog = (False, time_stamp)
        if list_proc_data[key].pid in running_table:
            list_proc_data[key].running = (True, time_stamp)
            list_proc_data[key].stopped = (False, time_stamp)
        print("FINAL START PROCESS FOR --->", list_proc_data[key])
        mutex_proc_dict.release()


def main (list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    print("MAIN STARTING CALLED")
    #Fork premiere execution
    newpid = main_exec(list_proc_data[key])

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    list_proc_data[key].pid = newpid
    list_proc_data[key].backlog = (True, time_stamp) #enter in starting process
    list_proc_data[key].stopped = (False, time_stamp) #not stopped anymore if mannually start or restart
    list_proc_data[key].fatal = (False, time_stamp) #not fatal anymore if restart or start
    list_proc_data[key].backoff_starting = (True, time_stamp) #starting 
    running_table[newpid]=list_proc_data[key]

    #envoi du thread starting process pour chaque process
    thread_starting_process = threading.Thread(target=starting_process, args=(list_proc_data, key, clients, running_table, mutex_proc_dict))
 #   thread_starting_process.daemon = True
    thread_list.append(thread_starting_process)
    thread_starting_process.start()

