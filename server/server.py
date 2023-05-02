import socket
import sys
import os
import select
from create_child_process import main as main_launch
from parse import main as main_parse

# Define the host and port to listen on
HOST = 'localhost'
PORT = 12345

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

client_proc_dict = {}
running = 1

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
            print("LAUNH SERVER HERE received WARNING IT LAUNCHES 5 WHILE: ", path_conf)
			#the first parsing for launch here
			


            list_proc_data = main_parse(path_conf, client_socket.fileno()) #ici retourner un element proc_data = process_data
            client_proc_dict[client_socket.fileno()]=list_proc_data
			#Boucler sur le tableau de structure de process du client a envoyer au launch
            for key in client_proc_dict[client_socket.fileno()]:
                main_launch(client_proc_dict[client_socket.fileno()][key])
            #main_launch(list_proc_data["while"]) #main_launch(process_structure)
            print("Key in dictionary ; ")
            print(client_proc_dict.keys())
    
            pid, status = os.waitpid(-1, os.WNOHANG)
            print(f"Process {pid} exited with status {status}")

	        #TEST faudrait checker la map de client/dico_process lol
				


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
            elif data == 'quit':
                print("Client quitting")
                result = "bye bitch"
                client_socket.sendall(result.encode())

                client_proc_dict.pop(client_socket.fileno())
                print("Key in dictionary left ; ")
                print(client_proc_dict.keys())

                poll_object.unregister(client_socket)
                clients.remove(client_socket)
                if len(client_proc_dict) == 0:
                    print("LEN OF CLIENT PROC DICT : ", len(client_proc_dict))
                    running = 0
                    break
				#client_socket.close()
            else:
                print("Invalid command.", data)
                result = "Invalid command."

            # Send the result back to the client
            client_socket.sendall(result.encode())

# Close the client connections and the server socket
for client in clients:
    poll_object.unregister(client)
    client.close()
server_socket.close()
