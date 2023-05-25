from start_launch import main as main_starting
#from server import is_exit_matching as is_exit_matching
from timestamp import *
import os
import signal
import calendar
import time

def is_exit_matching(status, process_data):
    exit_table = process_data.exitcodes
    match = 0
    for i in exit_table:
        if status == i:
            match = 1
    return match

def main(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list):
        #Check si c'est en backlog --> si oui rien faire (END)
        #else:
            #SI ca run PAS --> (et donci forcemment pas en backlog)
                #Si fatal
                    #Enlever fatal et restart a la main
                #Si stop gracefully ne rien faire (END)
                #Si crash  apres run mais pas auto restart (Gracefully deja ecarte)
                    #restart a la main
            #SI ca run 
                #Si auto restart
                    #Kill puis rien faire car autorestart
                #Sinon (Pas autorestart)
                    #kill gracefully
                    #main_starting a la main

    process = list_proc_data[key]
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.backlog[0] == True:
        print(timestamp('WARN') + "Process :" + key + " already in a start process\n", end="", flush=True)
        return "Process :" + key + " already in a start process"
    else:
        if process.running[0] == False:
            print(timestamp('WARN') + "Process :" + key + " is not running\n", end="", flush=True)
            return "Process :" + key + " is not running"
        else:
            if process.autorestart == True:
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
                return "Restart running Process :" + key
            else:
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

                process.cli_history.append('restart')
                process.stopping = (False, time_stamp)
                process.stopped = (False, time_stamp)
                process.quit_with_stop = False
                main_starting(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                print(timestamp('INFO') + "Restart running Process :" + key + "\n", end="", flush=True)
                return "Restart running Process :" + key
