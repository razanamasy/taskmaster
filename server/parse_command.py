import argparse
import sys
import io

#Define parent parser
parser = argparse.ArgumentParser(prog='Taskmaster', usage='%(prog)s [options]', add_help=False)
subparsers = parser.add_subparsers(dest='command')

# Subparser for "connexion" command
connexion_parser = subparsers.add_parser('connexion', help='Client connexion', add_help=False)

# Subparser for "start" command
start_parser = subparsers.add_parser('start', help='Start one stopped process or multiple processes', add_help=False)
start_parser.add_argument('process_name', nargs='+', type=str, help='Process names to restart')

# Subparser for "stop" command
stop_parser = subparsers.add_parser('stop', help='Stop one running process or multiple processes', add_help=False)
stop_parser.add_argument('process_name', nargs='+', type=str, help='Process names to stop')

# Subparser for "restart" command
restart_parser = subparsers.add_parser('restart', help='Restart one or multiple processes', add_help=False)
restart_parser.add_argument('process_name', nargs='+', type=str, help='Process names to restart')

# Subparser for "reload" command
reload_parser = subparsers.add_parser('reload', help='Reload configuration file', add_help=False)

# Subparser for "quit" command
quit_parser = subparsers.add_parser('quit', help='Quit the taskmaster server', add_help=False)

# Subparser for "status" command
status_parser = subparsers.add_parser('status', help='Status of all of your process', add_help=False)
status_parser.add_argument('process_name', nargs='*', type=str, help='Process names from which you want the status')

# Subparser for "help" command
status_parser = subparsers.add_parser('help', help='Display helper', add_help=False)

# Subparser for "shutdown" command
quit_parser = subparsers.add_parser('shutdown', help='Shutdown the taskmaster server', add_help=False)

def check_command_start(command):
    valid_commands = ["help", "reload", "start", "stop", "restart", "quit", "status", "shutdown", "connexion"]
    if any(command.startswith(cmd) for cmd in valid_commands):
        return True
    return False

def parse_command(command):
    cmd = {}
    cmd.clear()
    if check_command_start(command) == False:
        cmd["error"] = f"usage: Taskmaster [options]\nTaskmaster: error: argument command: invalid choice: '{command}' (choose from 'start', 'stop', 'restart', 'reload', 'quit', 'status', 'help', 'shutdown', 'connexion')"
        return (cmd)


    #parse command and it's arguments
    try:
        args, unknown_args = parser.parse_known_args(command.split())
        if args.command == "help":
            helper = io.StringIO()
            parser.print_help(file=helper)
            cmd[args.command] = helper.getvalue()
        elif args.command in ['start', 'stop', 'restart', 'status']:
            cmd[args.command] = args.process_name
        elif args.command in ['reload', 'quit', 'shutdown', 'connexion'] and unknown_args:
            cmd["error"] = f"Taskmaster: error: invalid argument: '{args.command}' should not have any arguments"
        elif args.command in ['reload', 'quit', 'shutdown', 'connexion'] and not unknown_args:
            cmd[args.command] = None
    except OSError as e:
        # Temporarily redirect stderr to capture the usage message
        original_stderr = sys.stderr
        sys.stderr = error_buffer = io.StringIO()
        try:
            parser.parse_args(command.split())
        except:
            pass
        sys.stderr = original_stderr

        # Retrieve the captured usage message
        usage_message = error_buffer.getvalue().strip()
        cmd["error"] = usage_message    
    return (cmd)
