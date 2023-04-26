import socket
import argparse

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345

# Create a socket object and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


while True:
    # Prompt the user for a command
    command = input('Enter a command ("start", "stop", or "quit"): ')

    print('loop 1')
    # Exit the loop if the user enters the quit command
    if command == 'quit':
        break

    print('loop 2')
    # Send the command to the server
    client_socket.sendall(command.encode())

    print('loop 3')
    # Receive the result from the server
    result = client_socket.recv(1024).decode()

    print('loop 4')
    # Print the result to the console
    print(result)

# Close the socket connection
print('end close')
client_socket.close()
