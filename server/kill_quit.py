import os
import signal

def main(client_fd, client_proc_dict, running_table):
	#TESTS	
    #client_proc_dict
    print("Killin pid of this quitting client : ", client_fd)
    for sub_value in client_proc_dict[client_fd]:
        print("Name of pid we will try to kill : ", client_proc_dict[client_fd][sub_value].name)
        print("IT's PID : ", client_proc_dict[client_fd][sub_value].pid)
        try:
            if (client_proc_dict[client_fd][sub_value].fatal == False):
                os.kill(client_proc_dict[client_fd][sub_value].pid, signal.SIGKILL)
                print(f"Process with PID {client_proc_dict[client_fd][sub_value].pid} exists. We can kill it")
            else:
                print("This shit is fatal")
        except ProcessLookupError:
            print(f"Process with PID {client_proc_dict[client_fd][sub_value].pid} does not exist.")
