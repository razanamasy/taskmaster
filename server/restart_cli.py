from start_launch import main as main_starting

def main(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list):
    #gestion erreur fonction
    if process.fatal == False:
        main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
    else:
        process.fatal == False
        main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
