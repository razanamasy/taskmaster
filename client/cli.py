import socket
import argparse
import sys

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345

# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('argument: ', sys.argv[1])
client_socket.sendall(sys.argv[1].encode())


while True:
    # Prompt the user for a command
    command = input('Enter a command ("start", "stop", or "quit"): ')

    # Send the command to the server
    client_socket.sendall(command.encode())

    # Receive the result from the server
    result = client_socket.recv(1024).decode()

    # Print the result to the console
    print(result)

    # Exit the loop if the user enters the quit command
    if command == 'quit':
        break

# Close the socket connection
print('end close')
client_socket.close()
