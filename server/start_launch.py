import calendar
import time
import threading
import copy
from create_child_process import main as main_exec
from threading import Thread, Lock

def starting_process(list_proc_data, key, clients, running_table, mutex_proc_dict):
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    list_proc_data[key].running = (False, time_stamp) #A delete car deja fait dans le monitor
    my_retries = copy.deepcopy(list_proc_data[key].startretries)
    while my_retries and (list_proc_data[key].running[0] == False):
        print("MY RETRIES = ", my_retries)
        my_retries -= 1
        time.sleep(list_proc_data[key].starttime)

        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)

        if len(clients) != 0: #Check also if has not been stopped to avoid revival process
            if list_proc_data[key].pid in running_table:
                list_proc_data[key].running = (True, time_stamp)
                list_proc_data[key].failure = (False, time_stamp)
                list_proc_data[key].backlog = (False, time_stamp)
                list_proc_data[key].stopped = (False, time_stamp)
                print("end of story for start pass to reload for : ", list_proc_data[key].name)
            else: #Fork
                print("Pid not in process_table, need to retry for :", list_proc_data[key].name)
                list_proc_data[key].backlog = (True, time_stamp)
                list_proc_data[key].failure = (True, time_stamp)
                #backoff_starting a true
                if my_retries == 0:
                    list_proc_data[key].fatal = (True, time_stamp)
                newpid = main_exec(list_proc_data[key])
                list_proc_data[key].pid = newpid
                list_proc_data[key].backoff_starting = (True, time_stamp) 
                running_table[newpid]=list_proc_data[key]
        else:
            break

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    if len(clients) != 0:
        mutex_proc_dict.acquire()
        print("NUMER RETRIES LEFT END OF WHILE", list_proc_data[key].startretries, "Failure is : ", list_proc_data[key].failure)
        if my_retries == 0 and list_proc_data[key].failure[0] == True:
            list_proc_data[key].fatal = (True, time_stamp)
            list_proc_data[key].backlog = (False, time_stamp)
        print("FINAL START PROCESS FOR --->", list_proc_data[key])
        mutex_proc_dict.release()


def main (list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
    print("MAIN STARTING CALLED")
    #Fork premiere execution
    newpid = main_exec(list_proc_data[key])

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    list_proc_data[key].pid = newpid
    list_proc_data[key].backlog = (True, time_stamp)
    list_proc_data[key].stopped = (False, time_stamp) 
    list_proc_data[key].backoff_starting = (True, time_stamp) 
    running_table[newpid]=list_proc_data[key]

    #envoi du thread starting process pour chaque process
    thread_starting_process = threading.Thread(target=starting_process, args=(list_proc_data, key, clients, running_table, mutex_proc_dict))
 #   thread_starting_process.daemon = True
    thread_list.append(thread_starting_process)
    thread_starting_process.start()

