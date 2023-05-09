import socket
import time
import sys
import os
import select
import copy
from create_child_process import main as main_launch
from start_launch import main as main_starting
from parse import main as main_parse
from kill_quit import main as kill_quit
import threading
from threading import Thread, Lock

# Define the host and port to listen on
HOST = 'localhost'
PORT = 12345

#SOCKET INITALISATION
# Create a socket object and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
def is_running():
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as err:
        print("Server already running")
        exit(1) 

is_running()
# Listen for incoming connections
server_socket.listen()

# Create a list to keep track of clients
clients = []

print(f"Server listening on {HOST}:{PORT}")

# Set up the poll object
poll_object = select.poll()
poll_object.register(server_socket, select.POLLIN)

#TABLES AND GLOBALE VARIABLES
#{pid : process}
running_table = {}
#{pid_timer: pid_exec}
timer_exec = {}
#{client : dico_process}
client_proc_dict = {}
#to quit
running = 1
#to start wait pid only at first connexion
first = 0
#Switch monitor deprecated
switch_monitor = [0]

#mutex
mutex_proc_dict = Lock()

def is_exit_matching(status, process_data):
    exit_table = process_data.exitcodes
    match = 0
    for i in exit_table:
        print(f"compare {status} with {i}")
        if status == i:
            print("It has matched !!!")
            match = 1
    return match

#WAIT PiD FORK and THREAD ICI ON ENLEVE DU TABLEAU PID
def wait_for_child(running_table, client_proc_dict):
        #   print("MONITOR HAS STARTED")
    while True:
    #    print("still in monitor but no running table")
        if bool(running_table):
    #        print("J'ai reussit a rentrer dans le monitor car In monitor, my running table SIZE is : ", len(running_table))
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if (pid != 0):
                        #    print(running_table[pid])
                    fd = running_table[pid].client
                    key = running_table[pid].name
                    #print(client_proc_dict[fd][key])
                    print("EST TU QUITTING ? ", running_table[pid].quitting)
                    if running_table[pid].quitting == True:
                        print("quitting do nothing in monitor")
							#  if fd in client_proc_dict:
							#client_proc_dict.pop(fd)
							#print("Key in dictionary left in monitor; ")
							#mutex_proc_dict.acquire()
							#mutex_proc_dict.release()

                    else:
                        restart = False
                        exit_match = is_exit_matching(status, running_table[pid])
                        if running_table[pid].autorestart == True:
                            restart = True
                        else:
                            if running_table[pid].autorestart == "unexpected" and exit_match == 0:
                                restart = True
				 #       print(f"MY RESTART VARIABLESSSS = {restart}")
                        print("INFO OF MY PROCESS THAT HAS BEEN KILLED", running_table[pid])
                        
                        #TEST FUCKING TEST
                        print(f"Backlog is : ", running_table[pid].backlog)
                        if running_table[pid].backlog == False:
                            print("Backlog false")
                            if running_table[pid].startretries != 0:
                                print("start retries diff 0")
                                if running_table[pid].autorestart == True:
                                    print("Auto restart true")
                                    if running_table[pid].stopping == False:
                                        print("not stopping")
                                        if restart == True:
                                            print("MY RESTART VARIABLESSSS = {restart}")

                        if running_table[pid].backlog == False and running_table[pid].startretries != 0 and (running_table[pid].autorestart == True or running_table[pid].autorestart == "unexpected") and running_table[pid].stopping == False and restart == True:
                            print(f"PLEAS GO IN MY RESTART {restart}")
                            main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict)

                    running_table.pop(pid)
                    print(f"Process {pid} exited with status {status}")
                    print("No longer waiting pid")
            except OSError as e:
                if e.errno == errno.ECHILD:
                       # No child processes to wait for
                    print("No child processes to wait for...")
                else:
                    # Some other error occurred
                    raise e
    print("MONITOR HAS QUIT")


while running:
    # Wait for events from clients or the server socket
    events = poll_object.poll()

    for fd, event in events:
        # If the event is from the server socket, it means there's a new connection
        if fd == server_socket.fileno():
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            poll_object.register(client_socket, select.POLLIN)
            print(f"New client connected from {addr[0]}:{addr[1]}")
            path_conf = client_socket.recv(1024).decode()
            #the first parsing for launch here
            

            list_proc_data = main_parse(path_conf, client_socket.fileno()) #ici retourner un element proc_data = process_data
            mutex_proc_dict.acquire()
            client_proc_dict[client_socket.fileno()]=list_proc_data
            mutex_proc_dict.release()
            

            #REPLICAS PUIS EXECUTION SORTIR CETTE FONCTION
            temp_dico = {}
            for key in client_proc_dict[client_socket.fileno()]:
                print(key)
                if client_proc_dict[client_socket.fileno()][key].numprocs > 1:
                    i = 1
                    while i < client_proc_dict[client_socket.fileno()][key].numprocs:
                        temp_dico[key + "-" + str(i)] = copy.deepcopy(client_proc_dict[client_socket.fileno()][key])
                        temp_dico[key + "-" + str(i)].name = key + "-" + str(i)
                        i += 1
            #CHECK DU NOUVEAU CLIENT DICO
            client_proc_dict[client_socket.fileno()].update(temp_dico)
            for key in client_proc_dict[client_socket.fileno()]:
                print(key)

            for key in client_proc_dict[client_socket.fileno()]:
                main_starting(client_proc_dict, client_socket.fileno(), key, running_table, mutex_proc_dict)

            #TESTS    
            #client_proc_dict
        #    print("value of pid of each client in dictionary ; ")
        #    for value in client_proc_dict:
        #        for sub_value in client_proc_dict[value]:
        #            print(client_proc_dict[value][sub_value].pid)
        #            print(client_proc_dict[value][sub_value].name)
            #Running process
        #    print("Key running table (should be modified in main_starting) ; ")
        #    print(running_table.keys())

            #START MONITOR DEATH ONLY AT START 
            print("switch monitor is at : ", switch_monitor[0])
            if first == 0:
                first = 1
                monitor = threading.Thread(target=wait_for_child, args=(running_table, client_proc_dict))
                monitor.daemon = True
                monitor.start()


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

            # Process the job command
            if data == 'start':
                print("Starting the job...")
                # Code to start the job goes here
                result = "starting the job..." 
            elif data == 'stop':
                print("Stopping the job...")
                # Code to stop the job goes here
                result = "Stopping the job..."
            elif data == 'quit': #TOUT LE PROCESS A THREAD si ca met du temp a kill ?
                print("Client quitting")
                result = "bye bitch"

                #kill all its process

                mutex_proc_dict.acquire()
                kill_quit(client_socket.fileno(), client_proc_dict, running_table)
                mutex_proc_dict.release()

                client_socket.sendall(result.encode())

                #TOUT CE MERDIER DOIT ETRE APPELE PAR LE MONITOR 

                if fd in client_proc_dict:
                    mutex_proc_dict.acquire()
                    client_proc_dict.pop(client_socket.fileno())
                    mutex_proc_dict.release()
                    print("Key in dictionary left ; ")
                    mutex_proc_dict.acquire()
                    print(client_proc_dict.keys())
                    mutex_proc_dict.release()

                poll_object.unregister(client_socket)
                clients.remove(client_socket)
			 #   mutex_proc_dict.acquire()
                if len(client_proc_dict) == 0:
                    print("LEN OF CLIENT PROC DICT : ", len(client_proc_dict))
                    running = 0
					#break
			#    mutex_proc_dict.release()
                #client_socket.close()
            else:
                print("Invalid command.", data)
                result = "Invalid command."

            # Send the result back to the client
            client_socket.sendall(result.encode())

print("salut g fini")
# Close the client connections and the server socket
for client in clients:
    poll_object.unregister(client)
    client.close()
server_socket.close()
