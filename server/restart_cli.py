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
    #gestion erreur fonction
    #Voir aussi le dernier exit code pour savoir si ca a ete stop gracefully
    process = client_proc_dict[fd][key]
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
    if process.backlog == True:
        print("Already in a start process")
        return
    else:
        if process.running == False:
            print("not running")
            if process.fatal == True:
                print("it's fatal")
                process.fatal = False
                process.cli_history.append('restart')
                process.stopping = False
                main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
            else:
                print("it'is NOT fatal")
              #  last_position = len(process.status_exit) - 1
                if is_exit_matching(process.status_exit[-1], process) == 0: #means it did not exit gracefully, here obviously autorestart = false because it's not in backlog
                    print("it has not exit gracefully")
                    process.cli_history.append('restart')
                    process.stopping = False
                    main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
        else:
            print("Running")
            if process.autorestart == True:
                print("Autorestart true so just kill")
                os.kill(process.pid, signal.SIGTERM)
            else:
                print("Autorestart false so kill and restart")
    			os.kill(process.pid, signal.process.stopsignal)
                process.cli_history.append('restart')
                process.stopping = False
                main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
