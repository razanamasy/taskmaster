import socket
import sys

#python server called with this config

for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])

# Define the host and port to listen on
HOST = 'localhost'
PORT = 12345

# Create a socket object and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

#replace with YAML parsing
conf_file = open(sys.argv[1], "r");
content = conf_file.read()



print(f"Server listening on {HOST}:{PORT}")
# Accept a new client connection
client_socket, addr = server_socket.accept()

#Here initialise the config file for the first time with YAML parsing command
#Loop on all programs listed on yaml
#test

while client_socket:

    print("New client connected from {addr[0]}:{addr[1]}")
    # Receive data from the client
    data = client_socket.recv(1024).decode()

    # Process the job command
    if data == 'start':
        print("Starting the job...")
        # Code to start the job goes here
        result = sys.argv[1]
    elif data == 'stop':
        print("Stopping the job...")
        # Code to stop the job goes here
        result = content
    elif data == 'quit':
        print("shutdown")
        result = "server shutdown"
        client_socket.sendall(result.encode())
        break
    else:
        print("Invalid command.")
        result = "Invalid command."

    # Send the result back to the client
    client_socket.sendall(result.encode())

# Close the client connection
server_socket.close()
conf_file.close()
