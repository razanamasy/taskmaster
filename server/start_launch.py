import calendar
import time
import threading
import copy
from create_child_process import main as main_exec
from threading import Thread, Lock

def starting_process(list_proc_data, key, clients, running_table, mutex_proc_dict):

    print("STARTING OF START PROCESS FOR --->", list_proc_data[key])
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    my_retries = copy.deepcopy(list_proc_data[key].startretries)

    mutex_proc_dict.acquire()
    last_starting = list_proc_data[key].backoff_starting[1] 
    mutex_proc_dict.release()
    while key in list_proc_data and time_stamp - last_starting <= list_proc_data[key].starttime and list_proc_data[key].stopped[0] == False:
        if len(clients) != 0 and list_proc_data[key].stopped[0] == False: #Check also if has not been stopped to avoid revival process
            mutex_proc_dict.acquire()
            if key not in list_proc_data or list_proc_data[key].fatal[0] == True:
                break
            mutex_proc_dict.release()
            if key in list_proc_data and list_proc_data[key].pid not in running_table:
                print("Pid not in process_table, need to retry for :", list_proc_data[key].name)
                if my_retries == 0:
                    print("But no retries left it's fataal:", list_proc_data[key].name)
                    list_proc_data[key].fatal = (True, time_stamp)
                    break

                mutex_proc_dict.acquire()
                if key in list_proc_data:
                       list_proc_data[key].backoff_starting = (False, time_stamp) 
                mutex_proc_dict.release()

                if key in list_proc_data:
                    time.sleep(list_proc_data[key].startretries - my_retries)

                mutex_proc_dict.acquire()
                if key not in list_proc_data:
                    mutex_proc_dict.release()
                    break

                if list_proc_data[key].stopped[0] == True:
                    print("YOOOOOOOOO IM STOPPED SO FUCK STARTING PROCESS HAHAHAHAHAHA")
                    list_proc_data[key].backlog = (False, time_stamp)
                    list_proc_data[key].exited = (False, time_stamp)
                    mutex_proc_dict.release()
                    break

         #       mutex_proc_dict.acquire()
                last_starting = list_proc_data[key].backoff_starting[1] 
          #      mutex_proc_dict.release()

                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)

         #       mutex_proc_dict.acquire()
                list_proc_data[key].backoff_starting = (True, time_stamp) #reset startsecs from last starting (substraction ts - b_s.ts)
         #       mutex_proc_dict.release()
                newpid = main_exec(list_proc_data[key])
                my_retries -= 1
                list_proc_data[key].pid = newpid
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
    list_proc_data[key].exit = (False, time_stamp) #not stopped anymore if mannually start or restart
    list_proc_data[key].fatal = (False, time_stamp) #not fatal anymore if restart or start
    list_proc_data[key].backoff_starting = (True, time_stamp) #starting 
    running_table[newpid]=list_proc_data[key]

    #envoi du thread starting process pour chaque process
    thread_starting_process = threading.Thread(target=starting_process, args=(list_proc_data, key, clients, running_table, mutex_proc_dict))
 #   thread_starting_process.daemon = True
    print(f"My key is : {key} the thread is : {thread_starting_process}")
    thread_list.append(thread_starting_process)
    thread_starting_process.start()

