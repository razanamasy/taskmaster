import socket
import argparse
import sys
import select
import signal
import readline
import curses
import textwrap
from client_utils import *

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
def main(stdscr):
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    flag = True
    try:
        client_socket.connect((HOST, PORT))
    except:
        flag = False
        return ()

    if len(sys.argv) == 2 and flag == True:
        if check_string(sys.argv[1]) == None:
            client_socket.sendall(sys.argv[1].encode())

            history_index = -1
            user_input = ''
            height, width = stdscr.getmaxyx()
            cmdy = stdscr.getyx()[0]

            stdscr.addstr('Taskmaster> ')
            stdscr.refresh()

            while True:

                # Check if the socket is ready to receive data
                readable, _, _ = select.select([client_socket, sys.stdin], [], [])

                for sock in readable:
                    if sock is client_socket:
                        # Receive and process server message
                        message = sock.recv(1024).decode()
                        if not message:
                            stdscr.addstr('Connection with server closed.\n')
                            stdscr.refresh()
                            return
                        else:
                            # Wrap the string to fit within the available space
                            wrapped_string = textwrap.fill(message, stdscr.getmaxyx()[1] - 1, replace_whitespace=False)

                            # Split the wrapped string into individual lines
                            lines = wrapped_string.split("\n")
                            stdscr.addstr('Received message from server:')
                            # Display the wrapped string
                            for line in lines:
                                stdscr.addstr(stdscr.getyx()[0] + 1, 0, line)
                                stdscr.refresh()
                            stdscr.addstr('\nTaskmaster> ')
                            stdscr.refresh()
                            cmdy = stdscr.getyx()[0]

                    elif sock is sys.stdin:
                        # Read user input from the user_input line
                        try:
                            c = stdscr.getch()
                            ### a faire !!! gerer le resize de la fenetre
                            if curses.is_term_resized(height, width):
                                stdscr.resize(stdscr.getmaxyx()[0], stdscr.getmaxyx()[1])
                            if c == curses.KEY_LEFT:
                                if stdscr.getyx()[0] == cmdy and stdscr.getyx()[1] > len('Taskmaster> '):
                                    stdscr.move(stdscr.getyx()[0], stdscr.getyx()[1] - 1)
                                    stdscr.refresh()
                                elif stdscr.getyx()[0] > cmdy:
                                    if stdscr.getyx()[1] == 0:
                                        stdscr.move(stdscr.getyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
                                        stdscr.refresh()
                                    else:
                                        stdscr.move(stdscr.getyx()[0], stdscr.getyx()[1] - 1)
                                        stdscr.refresh()
                            elif c == curses.KEY_RIGHT:
                                count = stdscr.getyx()[0] - cmdy
                                if stdscr.getyx()[1] < ((len('Taskmaster> ') + len(user_input)) - count * stdscr.getmaxyx()[1]) and stdscr.getyx()[1] < stdscr.getmaxyx()[1] - 1:
                                    stdscr.move(stdscr.getyx()[0], stdscr.getyx()[1] + 1)
                                    stdscr.refresh()
                                elif stdscr.getyx()[1] < ((len('Taskmaster> ') + len(user_input)) - count * stdscr.getmaxyx()[1]) and stdscr.getyx()[1] == stdscr.getmaxyx()[1] - 1:
                                    stdscr.move(stdscr.getyx()[0] + 1, 0)
                                    stdscr.refresh()
                            elif c == curses.KEY_UP:
                                if history_index < (len(command_history) - 1):
                                    history_index += 1
                                    stdscr.move(cmdy, len('Taskmaster> '))
                                    stdscr.clrtobot()
                                    stdscr.refresh()
                                    stdscr.addstr(command_history[len(command_history) - 1 - history_index])
                                    stdscr.refresh()
                                    user_input = command_history[len(command_history) - 1 - history_index]
                            elif c == curses.KEY_DOWN:
                                if history_index > -1:
                                    history_index -= 1
                                    if history_index != -1:
                                        stdscr.move(cmdy, len('Taskmaster> '))
                                        stdscr.clrtobot()
                                        stdscr.refresh()
                                        stdscr.addstr(command_history[history_index])
                                        stdscr.refresh()
                                        user_input = command_history[history_index]
                                    elif history_index == -1:
                                        stdscr.move(cmdy, len('Taskmaster> '))
                                        stdscr.clrtobot()
                                        stdscr.refresh()
                                        user_input = ''
                            elif c == curses.KEY_BACKSPACE or c == 127:
                                ### a fairei !!! gerer la deletion du dernier charatere d'une ligne au milieu d'un bloc multiligne
                                flag = False
                                if stdscr.getyx()[0] == cmdy and stdscr.getyx()[1] > len('Taskmaster> '):
                                    stdscr.delch(stdscr.getyx()[0], stdscr.getyx()[1] - 1)
                                    stdscr.refresh()
                                    flag = True
                                elif stdscr.getyx()[0] > cmdy:
                                    if stdscr.getyx()[1] == 0:
                                        stdscr.delch(stdscr.getyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
                                        stdscr.refresh()
                                        flag = True
                                    else:
                                        stdscr.delch(stdscr.getyx()[0], stdscr.getyx()[1] - 1)
                                        stdscr.refresh()
                                        flag = True
                                if flag == True:
                                    oldy, oldx = stdscr.getyx()
                                    stdscr.move(cmdy, len('Taskmaster> '))
                                    y, x = stdscr.getyx()
                                    new_input = ''
                                    while True:
                                        count = stdscr.getyx()[0] - cmdy
                                        if x < ((len('Taskmaster> ') + len(user_input) - 1) - count * stdscr.getmaxyx()[1]) and x < stdscr.getmaxyx()[1] - 1:
                                            char = stdscr.inch(y, x)
                                            new_input += (chr(char))
                                            x += 1
                                        elif x < ((len('Taskmaster> ') + len(user_input) - 1) - count * stdscr.getmaxyx()[1]) and x == stdscr.getmaxyx()[1] - 1:
                                            char = stdscr.inch(y, x)
                                            new_input += (chr(char))
                                            x = 0
                                            y += 1
                                        # Break the loop if we reached the end of the line
                                        if len(new_input) == len(user_input) - 1:
                                            break
                                    user_input = ''
                                    if new_input == ' ':
                                        new_input = ''
                                    user_input = new_input
                                    stdscr.move(oldy, oldx)
                            elif c == ord('\n'):
                                if len(user_input) > 0:
                                    command_history.append(user_input)
                                    history_index = -1

                                    # Send the user_input to the server
                                    client_socket.sendall(user_input.encode())
                                
                                    # Receive the result from the server
                                    result = client_socket.recv(1024).decode()

                                    # Exit the loop if the user enters the quit user_input
                                    if user_input == 'quit':
                                        return

                                    user_input = ''
                                    # Wrap the string to fit within the available space
                                    wrapped_string = textwrap.fill(result, stdscr.getmaxyx()[1] - 1, replace_whitespace=False)

                                    # Split the wrapped string into individual lines
                                    lines = wrapped_string.split("\n")
                                    
                                    # Display the wrapped string
                                    for line in lines:
                                        stdscr.addstr(stdscr.getyx()[0] + 1, 0, line)
                                        stdscr.refresh()
                                    stdscr.addstr('\nTaskmaster> ')
                                    stdscr.refresh()
                                    cmdy = stdscr.getyx()[0]
                                else:
                                    stdscr.addstr('\nTaskmaster> ')
                                    stdscr.refresh()
                                    cmdy = stdscr.getyx()[0]
                            else:
                                if len(chr(c)) == 1 and c != ord('\n'):
                                    ### a faire !!! insert where the prompt is
                                    stdscr.addstr(chr(c))
                                    stdscr.refresh()
                                    user_input += chr(c)
                        except EOFError:
                            user_input = "quit"

### a faire return error message des if else

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.cbreak() # enable reacting to keys instantly
    curses.noecho() # echoing of keys to the screen
    stdscr.nodelay(1) # getch() will be non-blocking
    stdscr.timeout(0) # if delay is zero, then non-blocking read is used, and getch() will return -1 if no input is waiting
    stdscr.keypad(True) # detect special keys
    stdscr.idlok(True) # enable line insertion/deletion optimizations for the window
    stdscr.scrollok(True) # enable automatic scrolling of the window when writing beyond the last line
    main(stdscr)
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()
    client_socket.close()
