import calendar
import time
import threading
import copy
from create_child_process import main as main_exec
from threading import Thread, Lock

def starting_process(list_proc_data, key, clients, running_table, mutex_proc_dict):

    print(f"{list_proc_data[key].name} entering in starting process", flush=True)
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    my_retries = copy.deepcopy(list_proc_data[key].startretries)
    my_retries_fix = copy.deepcopy(list_proc_data[key].startretries)
    my_starttime = copy.deepcopy(list_proc_data[key].starttime)
    my_curr_pid = copy.deepcopy(list_proc_data[key].pid)

    mutex_proc_dict.acquire()
    last_starting = list_proc_data[key].backoff_starting[1] 
    mutex_proc_dict.release()

    while key in list_proc_data and time_stamp - last_starting <= my_starttime and list_proc_data[key].stopped[0] == False:
        if len(clients) != 0 and list_proc_data[key].stopped[0] == False: #Check also if has not been stopped to avoid revival process
            mutex_proc_dict.acquire()
            if key not in list_proc_data or list_proc_data[key].fatal[0] == True:
               # list_proc_data[key].backlog = (False, time_stamp)
                mutex_proc_dict.release()
                break
            mutex_proc_dict.release()
            if key in list_proc_data and list_proc_data[key].pid not in running_table:
                print(f"starting process : pid not in process_table, need to retry for : {list_proc_data[key].name}", flush=True)
                if my_retries == 0:
                    print(f"No retries left for {list_proc_data[key].name} : FATAL ", flush=True)
                    list_proc_data[key].backlog = (False, time_stamp)
                    list_proc_data[key].fatal = (True, time_stamp)
                    break

                mutex_proc_dict.acquire()
                if key in list_proc_data:
                       list_proc_data[key].backoff_starting = (False, time_stamp) 
                mutex_proc_dict.release()

                if key in list_proc_data:
                    time.sleep(my_retries_fix - my_retries)

                mutex_proc_dict.acquire()
                if key not in list_proc_data or my_curr_pid in list_proc_data[key].obsolete_pid:
                    mutex_proc_dict.release()
                    break

                if list_proc_data[key].stopped[0] == True or my_curr_pid in list_proc_data[key].obsolete_pid:
                  #  print(f"in start launch the pid is obsolete {my_curr_pid} or stopped {key} so i don't continue starting process")
                    list_proc_data[key].backlog = (False, time_stamp)
                    list_proc_data[key].exited = (False, time_stamp)
                    mutex_proc_dict.release()
                    break

                last_starting = list_proc_data[key].backoff_starting[1]#reset the countdown starttime 

                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)

                list_proc_data[key].backoff_starting = (True, time_stamp) #reset startsecs from last starting (substraction ts - b_s.ts)
                newpid = main_exec(list_proc_data[key])
                my_retries -= 1
                list_proc_data[key].pid = newpid
                my_curr_pid = copy.deepcopy(list_proc_data[key].pid)
                running_table[newpid]=list_proc_data[key]
                mutex_proc_dict.release()
        else:
            break
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

    if key in list_proc_data and len(clients) != 0 and list_proc_data[key].stopped[0] == False:
        mutex_proc_dict.acquire()
        list_proc_data[key].backlog = (False, time_stamp)
        if list_proc_data[key].pid in running_table:
            list_proc_data[key].stopped = (False, time_stamp)
            list_proc_data[key].exited = (False, time_stamp)
            list_proc_data[key].running = (True, time_stamp)
        print(f"{list_proc_data[key].name} : leaving starting process", flush=True)
        mutex_proc_dict.release()


def main (list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    print(f"in start launch strating : {key}")

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if list_proc_data[key].starttime == 0:
        list_proc_data[key].backlog = (False, time_stamp)
        list_proc_data[key].exited = (False, time_stamp)
        list_proc_data[key].stopped = (False, time_stamp)
        list_proc_data[key].fatal = (False, time_stamp) #not fatal anymore if restart or start
        list_proc_data[key].running = (True, time_stamp)

    newpid = main_exec(list_proc_data[key])
    list_proc_data[key].pid = newpid
    running_table[newpid]=list_proc_data[key]

    if list_proc_data[key].starttime != 0:
        list_proc_data[key].backlog = (True, time_stamp) #enter in starting process
        list_proc_data[key].stopped = (False, time_stamp) #not stopped anymore if mannually start or restart
        list_proc_data[key].exit = (False, time_stamp) #not stopped anymore if mannually start or restart
        list_proc_data[key].fatal = (False, time_stamp) #not fatal anymore if restart or start
        list_proc_data[key].backoff_starting = (True, time_stamp) #starting 

        #envoi du thread starting process pour chaque process
        thread_starting_process = threading.Thread(target=starting_process, args=(list_proc_data, key, clients, running_table, mutex_proc_dict))
 #   thread_starting_process.daemon = True
        thread_list.append(thread_starting_process)
        thread_starting_process.start()
