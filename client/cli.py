import socket
import sys
import readline
import signal
sys.path.insert(0, '/home/alice/taskmaster/server/')
from parse_utils import *

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345

#command history list
command_history = []

# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def signal_handler(signal, frame):
    command = "quit"
    client_socket.sendall(command.encode())
    result = client_socket.recv(1024).decode()
    client_socket.close()
    exit(0)

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
        print('argument: ', sys.argv[1])
        if check_string(sys.argv[1]) == None:
            client_socket.sendall(sys.argv[1].encode())
            while True:
                # Prompt the user for a command
                if history_index == -1:
                    pass 
                else:
                    sys.stdout.write(command_history[history_index])

                sys.stdout.flush()  # Ensure the prompt is immediately displayed

                # Handle navigation through command history using readline
                command = ""
                while command == "":
                    try:
                        if history_index == -1:
                            command = input('Taskmaster> ')
                        else:
                            command = input('Taskmaster> ')
                            print(command)
                    except EOFError:
                        command = "quit"

                # Update command history
                command_history.append(command)
                history_index = -1
            
                try:
                    # Send the command to the server
                    client_socket.sendall(command.encode())

                    # Receive the result from the server
                    result = client_socket.recv(1024).decode()

                    # Print the result to the console
                    print(result)
                except:
                    print("Sorry server is closed")
                    command = 'quit'

                # Exit the loop if the user enters the quit command
                if command == 'quit':
                    break
        else:
            print("Use a valid path name")
    else:
        print("Wrong number of arguments")


    # Close the socket connection
    client_socket.close()
    return ()

if __name__ == "__main__":
    main()
