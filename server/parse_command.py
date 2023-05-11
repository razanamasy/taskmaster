import argparse

#Define parent parser
parser = argparse.ArgumentParser(prog='Taskmaster', usage='%(prog)s [options]')
subparsers = parser.add_subparsers(dest='command')

# Subparser for "start" command
start_parser = subparsers.add_parser('start', help='Start one stopped process or multiple processes')
start_parser.add_argument('process_name', nargs='+', type=str, help='Process names to restart')

# Subparser for "stop" command
stop_parser = subparsers.add_parser('stop', help='Stop one running process or multiple processes')
stop_parser.add_argument('process_name', nargs='+', type=str, help='Process names to stop')

# Subparser for "restart" command
restart_parser = subparsers.add_parser('restart', help='Restart one or multiple processes')
restart_parser.add_argument('process_name', nargs='+', type=str, help='Process names to restart')

# Subparser for "reload" command
reload_parser = subparsers.add_parser('reload', help='Reload configuration file')
reload_parser.add_argument('args', nargs=1, type=str, help='Configuration file path')

# Subparser for "quit" command
quit_parser = subparsers.add_parser('quit', help='Quit the taskmaster server')

# Subparser for "status" command
status_parser = subparsers.add_parser('status', help='Status of all of your process')

# Subparser for "help" command
status_parser = subparsers.add_parser('help', help='Display helper')

# Subparser for "shutdown" command
quit_parser = subparsers.add_parser('shutdown', help='Shutdown the taskmaster server')

def parse_command(command):
    cmd = {}
    #parse command and it's arguments
    try:
        args, unknown_args = parser.parse_known_args(command.split())
        if args.command == "help":
            cmd[args.command] = parser.print_help()
        elif args.command == "reload":
            cmd[args.command] = args.path
        elif args.command in ['start', 'stop', 'restart']:
            cmd[args.command] = args.process_name
        elif args.command in ['quit', 'status', 'shutdown']:
            cmd[args.command] = None
    except:
        if argparse.ArgumentError:
            cmd["error"] = argparse.ArgumentError
        elif argparse.ArgumentTypeError:
            cmd["error"] = argparse.ArgumentTypeError
        else:
            cmd["error"] = "Error invalid command"
    return (cmd)
