import socket
import calendar
import time
import sys
import signal 
import os
import select
import copy
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
import errno
from timestamp import *

#sys.stdout.flush()
#sys.stderr.flush()

# Define the host and port to listen on
HOST = "localhost"
try:
    PORT = int(sys.argv[2])
except:
    print(timestamp('CRIT') + "Bad port\n", end="", flush=True)
    exit(1)

if os.getuid() != 0:
    print(timestamp('CRIT') + "Error: you should be root to start a daemon Taskmaster server\n", end="", flush=True)
    exit(1)

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

def handle_sighup(signal, frame):
    new_list = main_parse(init_path_conf)
    for key in new_list:
        if key == "error":
            return("Error parsing : " + new_list[key])
    main_reload_cli(new_list, list_proc_data, mutex_proc_dict, clients, running_table, thread_list)
    return ("Reload succeded")
    
signal.signal(signal.SIGHUP, handle_sighup)

def is_running():
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as err:
        print(timestamp('ERRO') + f"Server error : {err}\n", end="", flush=True)
        exit(2) 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
is_running()
server_socket.listen()
print(timestamp('INFO') + f"Server listening on {HOST}:{PORT}\n", end="", flush=True)
poll_object = select.poll()
poll_object.register(server_socket, select.POLLIN)


def is_exit_matching(status, process_data):
    exit_table = process_data.exitcodes
    match = 0
    for i in exit_table:
        if status == i:
            match = 1
        else:
            print(timestamp('WARN') + f"Process {process_data.name} : has died unexpectedly\n", end="", flush=True)
    return match

def wait_for_child(running_table, list_proc_data, clients, thread_list):
    while True:
        if len(clients) == 0:
            break
        if bool(running_table):
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if (pid < 0):
                    print(timestamp('WARN') + f"child :{pid} encountered error\n", end="", flush=True)
                else:
                    if (pid > 0):
                        # Close file descriptors
                        stdout_original = sys.stdout
                        stderr_original = sys.stderr
                        stdout_fd = os.dup(stdout_original.fileno())
                        stderr_fd = os.dup(stderr_original.fileno())
                        if running_table[pid].stdout_fd != -1:
                            os.close(running_table[pid].stdout_fd)
                        if running_table[pid].stderr_fd != -1:
                            os.close(running_table[pid].stderr_fd)

                        # Restore original file descriptors and sys.stdout/sys.stderr
                        if stdout_fd is not None:
                            os.dup2(stdout_fd, running_table[pid].stdout_og)
                            os.close(stdout_fd)
                        if stderr_fd is not None:
                            os.dup2(stderr_fd, running_table[pid].stderr_og)
                            os.close(stderr_fd)
                        sys.stdout = stdout_original
                        sys.stderr = stderr_original

                        current_GMT = time.gmtime()
                        time_stamp = calendar.timegm(current_GMT)

                        key = running_table[pid].name
                        running_table[pid].running = (False, time_stamp)
                        running_table[pid].stopping = (False, time_stamp) 

                        #STOPPED OU EXIT ?
                        if running_table[pid].quit_with_stop == True:
                            print(timestamp('INFO') +  f"STOP detection in monitor {running_table[pid].name}\n", end="", flush=True)
                            running_table[pid].stopped = (True, time_stamp)
                            running_table[pid].stopping = (False, time_stamp)
                            running_table[pid].backlog = (False, time_stamp)
                            running_table[pid].exited = (False, time_stamp)
                        else:
                            print(timestamp('INFO') +  f"EXIT detection in monitor {running_table[pid].name}\n", end="", flush=True)
                            running_table[pid].stopped = (False, time_stamp)
                            running_table[pid].stopping = (False, time_stamp)
                            running_table[pid].exited = (True, time_stamp)
                        
                        restart = False
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
                        print(timestamp('INFO') + f"Process {pid} exited with status {status}\n", end="", flush=True)
            except OSError as e:
                if e.errno == errno.ECHILD:
                    pass
                else:
                    print(timestamp('CRIT') + "error waitpid\n", end="", flush=True)
                    raise e
    print(timestamp('INFO') + "MONITOR HAS QUIT\n", end="", flush=True)


def launching(running, list_proc_data, clients, running_table, first, thread_list, path_conf):
    #CHECK REPLICAS
    temp_dico = {}
    for key in list_proc_data:
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

while running:
    # Wait for events from clients or the server socket
    events = poll_object.poll()

    for fd, event in events:
        # NEW CONNEXION 
        if fd == server_socket.fileno():
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            poll_object.register(client_socket, select.POLLIN)
            print(timestamp('INFO') + f"New client connected from {addr[0]}:{addr[1]}\n", end="", flush=True)


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
            if cmd_key == 'connexion':
                error = 0
                result = "Already connected..\n"
                # First launch process and monitor calling (only once)
                if first == 0:
                    result = "Connexion to server...\n"
                    first = 1
                    list_proc_data = copy.deepcopy(main_parse(init_path_conf))
                    for key in list_proc_data:
                        if key == "error":
                            error = 1
                            result = list_proc_data[key] 
                            result += ": Closing server\x03"
                            client_socket.sendall(result.encode())
                            running = 0
                            break
                    if error == 0:
                        launching(running, list_proc_data, clients, running_table, first, thread_list, sys.argv[1])
                        time.sleep(0.5)
                        for key in list_proc_data:
                                # print(f"STATUS OF {list_proc_data[key]}")
                            curr_status = main_status_cli(list_proc_data, key, mutex_proc_dict)
                            result +=  "Process : " + key + " : " + curr_status[0]  + " since : " + str(curr_status[1]) + " seconds "  + "\n"
                    else:
                        break

            elif cmd_key == 'start':
                print(timestamp('INFO') + "starting called by client " + str(client.fileno()) + "\n", end="", flush=True)
                result = "starting called..." 
                for key in cmd['start']:
                    if key in list_proc_data:
                        result = main_start_cli(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                    else:
                        result = "Can start process :" + key + ", it does not exist"
                        print(timestamp('WARN') + result + "\n", end="", flush=True)

                # Code to start the job goes here
            elif cmd_key == 'stop':
                print(timestamp('INFO') + "Stopping called by client " + str(client.fileno()) + "\n", end="", flush=True)
                result = "Stopping called..."
                for key in cmd['stop']:
                    if key in list_proc_data:
                        result = main_stop_cli(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                    else:
                        result = "Can't stop process :" + key + ", it does not exist"
                        print(timestamp('WARN') + result + "\n", end="", flush=True)
            elif cmd_key == 'restart':
                print(timestamp('INFO') + "restarting called by client " + str(client.fileno()) + "\n", end="", flush=True)
                result = "restarting called..."
                for key in cmd['restart']:
                    if key in list_proc_data:
                        result = main_restart_cli(list_proc_data, key, clients, running_table, mutex_proc_dict, thread_list)
                    else:
                        result = "Can't restart process :" + key + ", it does not exist"
                        print(timestamp('WARN') + result + "\n", end="", flush=True)
            elif cmd_key == 'reload':
                result = "Reloading the configuration file : " + init_path_conf 
                result = handle_sighup(signal.SIGHUP, None)
              #  new_list = main_parse(init_path_conf)
              #  main_reload_cli(new_list, list_proc_data, mutex_proc_dict, clients, running_table, thread_list)

            elif cmd_key == 'status':
                result = "------STATUS------\n"
                if len(cmd['status']) == 0:
                    for key in list_proc_data:
							# print(f"STATUS OF {list_proc_data[key]}")
                        curr_status = main_status_cli(list_proc_data, key, mutex_proc_dict)
                        result +=  "Process : " + key + " : " + curr_status[0]  + " since : " + str(curr_status[1]) + " seconds "  + "\n"
                else:
                    for key in cmd['status']:
                        if key in list_proc_data:
                            curr_status = main_status_cli(list_proc_data, key, mutex_proc_dict)
                            result +=  "Process : " + key + " :" + curr_status[0]  + " since : " + str(curr_status[1]) + " seconds "  + "\n"
                        else:
                            result = "Can't get status of process : " + key + ", it does not exist"
                            print(timestamp('WARN') + result + "\n", end="", flush=True)
                print(result, end="", flush=True)
            elif cmd_key == 'help':
                print(timestamp('INFO') + "Displaying helper requested by client  " + str(client.fileno()) + "\n", end="", flush=True)
                result = str(cmd["help"])
            elif cmd_key == 'quit': 
                print(timestamp('INFO') + "Client " + str(client.fileno()) + " quitting\n", end="", flush=True)
                result = None
                #Remove client from everything
                poll_object.unregister(client_socket)
                clients.remove(client_socket)

                if len(clients) == 0:
                    kill_quit(list_proc_data, running_table, mutex_proc_dict)
                    running = 0
            elif cmd_key == 'shutdown':
                print(timestamp('INFO') + "SERVER SHUTTING DOWN...\n", end="", flush=True)
                result = "Server shutdown"
                mutex_proc_dict.acquire()
                while len(clients) != 0:
                    poll_object.unregister(clients.pop())
                    print(timestamp('INFO') + f"client left: {clients} \n", end="", flush=True)
                mutex_proc_dict.release()

                if len(clients) == 0:
                    kill_quit(list_proc_data, running_table, mutex_proc_dict)
                    running = 0

            else:
                print(timestamp('ERRO') + "Wrong command: " + data + "\n", end="", flush=True)
                result = cmd[cmd_key]

            if result != None:
                # Send the result back to the client
                result += '\x03'
                client_socket.sendall(result.encode())
            else:
                pass

for thread in thread_list:
    thread.join()

for client in clients:
    poll_object.unregister(client)
    client.close()
server_socket.close()
