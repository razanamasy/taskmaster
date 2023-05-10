import socket
import sys
import readline
sys.path.insert(0, '/home/alice/taskmaster/server/')
from parse_utils import *

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345


# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    #command history list
    command_history = []
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
                    sys.stdout.write('Taskmaster> ')
                else:
                    sys.stdout.write('Taskmaster> ')
                    sys.stdout.write(command_history[history_index])

                sys.stdout.flush()  # Ensure the prompt is immediately displayed

                # Handle navigation through command history using readline
                if history_index == -1:
                    command = input()
                else:
                    command = input()
                    print(command)

                # Update command history
                command_history.append(command)
                history_index = -1
                        
                # Send the command to the server
                client_socket.sendall(command.encode())

                # Receive the result from the server
                result = client_socket.recv(1024).decode()

                # Print the result to the console
                print(result)

                # Exit the loop if the user enters the quit command
                if command == 'quit':
                    break
        else:
            print("Use a valid path name")
    else:
        print("Wrong number of arguments")


    # Close the socket connection
    print('end close')
    client_socket.close()
    return ()

if __name__ == "__main__":
    main()
