from create_child_process import main as main_exec

def main(client_proc_dict, fd, key, running_table):
    newpid = main_exec(client_proc_dict[fd][key]);
    print("client : ", fd, " process name : ", key, " pid is : ", newpid)
    client_proc_dict[fd][key].pid = newpid;
    running_table[newpid]=client_proc_dict[fd][key];
