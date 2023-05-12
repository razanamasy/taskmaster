import socket
import argparse
import sys
import select
import signal
import readline
sys.path.insert(0, '/home/hrazanam/taskmaster/server/')
from parse_utils import *

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345

#command history list
command_history = []

# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def signal_handler(signal, frame):
    user_input = "quit"
    client_socket.sendall(user_input.encode())
    result = client_socket.recv(1024).decode()
    client_socket.close()
    exit(0)

# Function to handle user input and receive messages from the server
def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    history_index = -1
    flag = True
    try:
        client_socket.connect((HOST, PORT))
    except:
        flag = False
        print("No available Takmaster server")
        return ()

    if len(sys.argv) == 2 and flag == True:
        if check_string(sys.argv[1]) == None:
            client_socket.sendall(sys.argv[1].encode())
            while True:
                # Prompt the user for a user_input
                if history_index == -1:
                    pass
                else:
                    sys.stdout.write(user_input_history[history_index])

                sys.stdout.flush()  # Ensure the prompt is immediately displayed
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
                        # Read user input from the user_input line
                        try:
                            if history_index == -1:
                                user_input = input('Taskmaster> ')
                            else:
                                user_input = input('Taskmaster> ')
                                print(user_input)
                        except EOFError:
                            user_input = "quit"

                        # Update command history
                        command_history.append(user_input)
                        history_index = -1

                        # Send the user_input to the server
                        client_socket.sendall(user_input.encode())

                        # Receive the result from the server
                        result = client_socket.recv(1024).decode()

                        # Print the result to the console
                        print(result)

                        # Exit the loop if the user enters the quit user_input
                        if user_input == 'quit':
                            return

# Print the initial prompt before entering the loop
print('Taskmaster> ')

if __name__ == "__main__":
    main()
    print('End connection')
    client_socket.close()
