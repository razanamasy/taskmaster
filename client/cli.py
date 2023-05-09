import socket
import argparse
import sys
import readline
sys.path.insert(0, '/home/alice/taskmaster/server/')
from parse_utils import *

# Define the host and port to connect to
HOST = 'localhost'
PORT = 12345

#command history list
command_history = []
history_index = -1

# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Define parent parser
parser = argparse.ArgumentParser(prog='Taskmaster', usage='%(prog)s [options]')
subparsers = parser.add_subparsers(dest='command')

# Subparser for "start" command
start_parser = subparsers.add_parser('start', help='Start one stopped process or multiple processes')
start_parser.add_argument('process name', nargs='+', type=str, help='Process names to restart')

# Subparser for "stop" command
stop_parser = subparsers.add_parser('stop', help='Stop one running process or multiple processes')
stop_parser.add_argument('process name', nargs='+', type=str, help='Process names to stop')

# Subparser for "restart" command
restart_parser = subparsers.add_parser('restart', help='Restart one or multiple processes')
restart_parser.add_argument('process name', nargs='+', type=str, help='Process names to restart')

# Subparser for "reload" command
reload_parser = subparsers.add_parser('reload', help='Reload configuration file')
reload_parser.add_argument('path', nargs=1, type=str, help='Configuration file path')

# Subparser for "quit" command
quit_parser = subparsers.add_parser('quit', help='Quit the taskmaster server')

# Subparser for "status" command
status_parser = subparsers.add_parser('status', help='Status of all of your process')

# Subparser for "help" command
status_parser = subparsers.add_parser('help', help='Display helper')

try:
    client_socket.connect((HOST, PORT))
    if len(sys.argv) == 2:
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

                #parse command and it's arguments
                try:
                    args = parser.parse_args(command.split())
                except (argparse.ArgumentError, SystemExit):
                    continue

                # Validate command and arguments
                if args.command in ['start', 'stop', 'restart', 'reload'] and not args.args:
                    print(f'Error: {args.command} command requires at least one argument')
                    continue
                elif args.command in ['quit', 'status'] and args.args:
                    print(f'Error: {args.command} command should not have any arguments')
                    continue
                else:
                    if args.command != "help":
                        # Send the command to the server
                        #client_socket.sendall(args.command.encode())

                        # Receive the result from the server
                        result = client_socket.recv(1024).decode()

                        # Print the result to the console
                        print(result)

                        # Exit the loop if the user enters the quit command
                        if args.command == 'quit':
                            break
                    else:
                        parser.print_help()

        else:
            print("Use a valid path name")
    else:
        print("Wrong number of arguments")
except:
    print("No available taskmaster server")

# Close the socket connection
print('end close')
client_socket.close()
