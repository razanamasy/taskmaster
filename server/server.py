import socket
import calendar
import time
import sys
import signal 
import os
import select
import copy
#from create_child_process import main as main_launch
from start_launch import main as main_starting
from restart_cli import main as main_restart_cli
from stop_cli import main as main_stop_cli
from start_cli import main as main_start_cli
from status_cli import main as main_status_cli
from reload_cli import main as main_reload_cli
from parse import main as main_parse
from kill_quit import main as kill_quit
import threading
from threading import Thread, Lock
from parse_command import *
import ctypes

# Define the host and port to listen on
HOST = sys.argv[2] 
PORT = int(sys.argv[3])

#SOCKET INITALISATION
# Create a socket object and bind it to the host and port

# Create a list to keep track of clients
clients = []
#TABLES AND GLOBALE VARIABLES
#{pid : process}
running_table = {}
#{name_key : process}
list_proc_data = {}
#{client : dico_process}
#client_proc_dict = {}
#to quit
running = 1
#to start wait pid only at first connexion
first = 0
#Switch monitor deprecated
switch_monitor = [0]
#Thread tables
thread_list = []
#Initil path conf in case of reload
init_path_conf = sys.argv[1]
#mutex
mutex_proc_dict = Lock()

#signal.signal(signal.SIGHUP, main_reload_cli)

def is_running():
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as err:
        print("Server already running")
        exit(1) 


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
is_running()
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")
poll_object = select.poll()
poll_object.register(server_socket, select.POLLIN)


def is_exit_matching(status, process_data):
    print("Is exit in server monitoring")
    exit_table = process_data.exitcodes
    match = 0
    for i in exit_table:
        print(f"compare {status} with {i}")
        if status == i:
            print("It has matched !!!")
            match = 1
    return match

#WAIT PiD FORK and THREAD ICI ON ENLEVE DU TABLEAU PID
def wait_for_child(running_table, list_proc_data, clients, thread_list):
    while True:
        if len(clients) == 0:
            print("LEN OF CLIENTS MONITOR : ", len(clients))
            break
        if bool(running_table):
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if (pid < 0):
                    print(f"child :{pid} encountered error")
                else:
                    if (pid > 0):
                        current_GMT = time.gmtime()
                        time_stamp = calendar.timegm(current_GMT)

                        key = running_table[pid].name
                        running_table[pid].status_exit.append(status)
                        running_table[pid].running = (False, time_stamp)
                        running_table[pid].stopping = (False, time_stamp) 

                        #STOPPED OU EXIT ?
                        if running_table[pid].quit_with_stop == True:
                            running_table[pid].stopped = (True, time_stamp)
                            running_table[pid].backlog = (False, time_stamp)
                            running_table[pid].exited = (False, time_stamp)
                        else:
                            running_table[pid].stopped = (False, time_stamp)
                            running_table[pid].exited = (True, time_stamp)
                        
                        restart = False
                      #  print("INFO OF MY PROCESS THAT HAS BEEN KILLED", running_table[pid])
                        if running_table[pid].quitting == False and running_table[pid].quit_with_stop == False:
                            exit_match = is_exit_matching(status, running_table[pid])
                            if running_table[pid].autorestart == True:
                                restart = True
                            else:
                                if running_table[pid].autorestart == "unexpected" and exit_match == 0:
                                    restart = True

                            if running_table[pid].backlog[0] == False and running_table[pid].fatal[0] == False and restart == True:
                                main_starting(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)

                        running_table.pop(pid)
                        print(f"Process {pid} exited with status {status}")
                        print("No longer waiting pid")
            except OSError as e:
                if e.errno == errno.ECHILD:
                    print("No child processes to wait for...")
                else:
                    print("WAITPID HAS CRASHED I DUNNO WHY IN MONITOR")
                    raise e
    print("MONITOR HAS QUIT")


def launching(running, list_proc_data, clients, running_table, first, thread_list, path_conf):
    #CHECK REPLICAS
    temp_dico = {}
    for key in list_proc_data:
        print(key)
        if list_proc_data[key].numprocs > 1:
            i = 1
            while i < list_proc_data[key].numprocs:
                temp_dico[key + "-" + str(i)] = copy.deepcopy(list_proc_data[key])
                temp_dico[key + "-" + str(i)].name = key + "-" + str(i)
                temp_dico[key + "-" + str(i)].numprocs = 1
                i += 1
    #UPDATE PROCES TO RUN
    list_proc_data.update(temp_dico)
    #FIRT EXEC IF AUTOSTART
    for key in list_proc_data:
        if list_proc_data[key].autostart == True:
            main_starting(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)

    monitor = threading.Thread(target=wait_for_child, args=(running_table, list_proc_data, clients, thread_list))
    monitor.daemon = True
    monitor.start()
    thread_list.append(monitor)
    print("In launching keys are : ", list_proc_data.keys())




while running:
    # Wait for events from clients or the server socket
    events = poll_object.poll()

    for fd, event in events:
        # NEW CONNEXION 
        if fd == server_socket.fileno():
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            poll_object.register(client_socket, select.POLLIN)
            print(f"New client connected from {addr[0]}:{addr[1]}")
        
            # First launch process and monitor calling (only once)
            if first == 0:
                first = 1
                print(f"path conf = {init_path_conf}")
                list_proc_data = copy.deepcopy(main_parse(init_path_conf))
                print("in list proc data :: ", list_proc_data.keys())
                launching(running, list_proc_data, clients, running_table, first, thread_list, sys.argv[1])
                print("after launching the keys in dico are : ", list_proc_data.keys())


        # If the event is from a client socket, it means there's data to read
        elif event & select.POLLIN:
            client_socket = None
            for client in clients:
                if client.fileno() == fd:
                    client_socket = client
                    break
            if client_socket is None:
                continue

            data = client_socket.recv(1024).decode()
            cmd = parse_command(data)

            cmd_key = next(iter(cmd.keys()))

            # Process the job command
            if cmd_key == 'start':
                print("Starting the job...")
                result = "starting called..." 
                for key in cmd['start']:
                    if key in list_proc_data:
                        result = main_start_cli(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                    else:
                        result = "Can start process :" + key + ", it does not exist"

                # Code to start the job goes here
            elif cmd_key == 'stop':
                print("Stopping the job...")
                result = "Stopping called..."
                for key in cmd['stop']:
                    if key in list_proc_data:
                        result = main_stop_cli(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                    else:
                        result = "Can't stop process :" + key + ", it does not exist"
                # Code to stop the job goes here
            elif cmd_key == 'restart':
                print(f"cmd_key for restart is {cmd_key}")
                result = "restarting called..."
                for key in cmd['restart']:
                    if key in list_proc_data:
                        result = main_restart_cli(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                    else:
                        result = "Can't restart process :" + key + ", it does not exist"
                # Code to stop the job goes here
            elif cmd_key == 'reload':
                print("Reloading the configuration file..." + init_path_conf)
                result = "Reloading the configuration file : " + init_path_conf 
                new_list = main_parse(init_path_conf)
                print(f"New list is : {new_list}")
                print(f"Old list is : {list_proc_data}")
             #   handle_sighup(signal.SIGHUP, None)
                main_reload_cli(new_list, list_proc_data, mutex_proc_dict, clients, running_table, thread_list)

            elif cmd_key == 'status':
                result = "------STATUS------\n"
                for key in list_proc_data:
                    curr_status = main_status_cli(list_proc_data, key, mutex_proc_dict)
                    result +=  "Process :" + key + " :" + curr_status[0]  + " since : " + str(curr_status[1]) + " seconds "  + "\n"
                # Code to stop the job goes here
            elif cmd_key == 'help':
                print("Display helper...")
                # Code to stop the job goes here
                result = str(cmd["help"]) 
            elif cmd_key == 'quit': #TOUT LE PROCESS A THREAD si ca met du temp a kill ?
                print("Client quitting")
                result = "\x03"
                #Remove client from everything
            #    client_socket.sendall(result.encode())
                poll_object.unregister(client_socket)
                clients.remove(client_socket)

                #If last client
		   #     mutex_proc_dict.acquire()
                if len(clients) == 0:
                    #Kill all processes
                    kill_quit(list_proc_data, running_table, mutex_proc_dict)
                    print("LEN OF CLIENTS : ", len(clients))
                    running = 0
		   #     mutex_proc_dict.release()
            elif cmd_key == 'shutdown':
                print("SHUTDOWN")
                result = "shutdown"
                print(f"Len of clients : {clients} ")
                #kill all process 
                #Clear clients
                mutex_proc_dict.acquire()
                while len(clients) != 0:
                    poll_object.unregister(clients.pop())
                    print(f"client left: {clients} ")
                mutex_proc_dict.release()

                print(f"Len of clients : {len(clients)} ")
			 #   mutex_proc_dict.acquire()
                if len(clients) == 0:
                    print("CLIENT LEN IS EMPTY")
                    kill_quit(list_proc_data, running_table, mutex_proc_dict)
                    print("LEN OF CLIENTS : ", len(clients))
                    running = 0
			 #   mutex_proc_dict.release()

            else:
                print("Invalid command.", data)
                result = cmd[cmd_key] 

            # Send the result back to the client
            result += '\x03'
            client_socket.sendall(result.encode())

for thread in thread_list:
    print(f"here is my thread : {thread}")
#    if thread.is_alive():
#        return
    thread.join()

for client in clients:
    poll_object.unregister(client)
    client.close()
server_socket.close()
