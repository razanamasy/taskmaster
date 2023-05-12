import socket
import argparse
import sys
import select

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345

# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('argument: ', sys.argv[1])
client_socket.sendall(sys.argv[1].encode())

# Function to handle user input and receive messages from the server
def handle_input_and_receive():
    while True:
        # Check if the socket is ready to receive data
        readable, _, _ = select.select([client_socket, sys.stdin], [], [])

        for sock in readable:
            if sock is client_socket:
                # Receive and process server message
                message = sock.recv(1024).decode()
                if not message:
                    print("Connection with server closed.")
                    return
                else:
                    print("Received message from server:", message)
            elif sock is sys.stdin:
                # Read user input from the command line
                user_input = input('Enter a command ("start", "stop", or "quit"): ')

                # Send the command to the server
                client_socket.sendall(user_input.encode())

                # Receive the result from the server
                result = client_socket.recv(1024).decode()

                # Print the result to the console
                print(result)

                # Exit the loop if the user enters the quit command
                if user_input == 'quit':
                    return

# Print the initial prompt before entering the loop
print('Enter a command ("start", "stop", or "quit"):')

# Call the function to handle user input and receive messages
handle_input_and_receive()

# Close the socket connection
print('End connection')
client_socket.close()
