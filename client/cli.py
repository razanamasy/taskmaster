import socket
import sys
import readline
import signal

# Define the host and port to connect to
HOST = "localhost"
try:
    PORT = int(sys.argv[1])
except:
    print("Bad port")

#command history list
command_history = []

# Create a socket object and connect to the server and send the path file to launch
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def signal_handler(signal, frame):
    try:
        client_socket.sendall(command.encode())
    except:
        pass
    client_socket.close()
    exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGALRM, signal_handler)
    history_index = -1
    flag = True
    try:
        client_socket.connect((HOST, PORT))
        command = 'connexion'
        client_socket.sendall(command.encode())
        result = client_socket.recv(1024).decode()
        print(result)
    except OSError as e:
        flag = False
        print(f"Client : Taskmaster server not available : {str(e)}")
        return ()

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

            signal.alarm(5)
            if command != 'quit':
                result = ''
                # Receive the result from the server
                while True:
                    chunk = client_socket.recv(1024).decode()
                    result += chunk
                    if '\x03' in chunk:
                        break
                # Print the result to the console
                if result:
                    print(result)
            signal.alarm(0)
        except:
            print("Sorry server is closed")
            command = 'quit'

        # Exit the loop if the user enters the quit command
        if command == 'quit':
            break

    # Close the socket connection
    client_socket.close()
    return ()

if __name__ == "__main__":
    main()
