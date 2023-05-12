import yaml
import sys
import os
from process_struct import *
from parse_utils import *

error = {}
conf_list = ["cmd", "numprocs", "umask", "workingdir", "autostart", "autorestart", "exitcodes", "startretries", "starttime", "stopsignal", "stoptime", "stdout", "stderr", "env"]
signals = {"TERM": "SIGTERM", "HUP": "SIGHUP", "INT": "SIGINT", "QUIT": "SIGQUIT", "KILL": "SIGKILL", "USR1": "SIGUSR1", "USR2": "SIGUSR2"}
int_signals = {15: "SIGTERM", 1: "SIGHUP", 2: "SIGINT", 3: "SIGQUIT", 9: "SIGKILL", 10: "SIGUSR1", 12: "SIGUSR2"}

def check_value_types(key, value):
    error_flag = None 
    if key == "cmd":
        error_flag = check_string(value)
        if error_flag != None:
            error_flag = "error: cmd " + error_flag
            return (error_flag)
    if key == "numprocs":
        error_flag = check_int(value, 1, 10)
        if error_flag != None:
            error_flag = "error: numprocs " + error_flag
            return (error_flag)
    if key == "umask":
        error_flag = check_umask(value)
        if error_flag != None:
            error_flag = "error: umask " + error_flag
            return (error_flag)
    if key == "workingdir":
        error_flag = check_string(value)
        if error_flag != None:
            error_flag = "error: workingdir " + error_flag
            return (error_flag)
    if key == "autostart":
        error_flag = check_bool(value)
        if error_flag != None:
            error_flag = "error: autostart " + error_flag
            return (error_flag)
    if key == "autorestart":
        error_flag = check_autorestart(value)
        if error_flag != None:
            error_flag = "error: autorestart " + error_flag
            return (error_flag)
    if key == "exitcodes":
        error_flag = check_exitcodes(value)
        if error_flag != None:
            error_flag = "error: exitcodes " + error_flag
            return (error_flag)
    if key == "startretries":
        error_flag = check_int(value, 0, 50)
        if error_flag != None:
            error_flag = "error: startretries " + error_flag
            return (error_flag)
    if key == "starttime":
        error_flag = check_int(value, 0, 3600)
        if error_flag != None:
            error_flag = "error: startime " + error_flag
            return (error_flag)
    if key == "stopsignal":
        error_flag = check_stopsignal(value)
        if error_flag != None:
            error_flag = "error: stopsignal " + error_flag
            return (error_flag)
    if key == "stoptime":
        error_flag = check_int(value, 0, 60)
        if error_flag != None:
            error_flag = "error: stoptime " + error_flag
            return (error_flag)
    if key == "stdout":
        error_flag = check_string(value)
        if error_flag != None:
            error_flag = "error: stdout " + error_flag
            return (error_flag)
    if key == "stderr":
        error_flag = check_string(value)
        if error_flag != None:
            error_flag = "error: stderr " + error_flag
            return (error_flag)
    if key == "env":
        error_flag = check_env(value)
        if error_flag != None:
            error_flag = "error: env " + error_flag
            return (error_flag)
    return (error_flag)

def set_attribute(process_dict, key, value):
    if key == "autostart" or key == "autorestart":
        if value == "false":
            value = False
        elif value == "true":
            value = True
    elif key == "stopsignal":
        if isinstance(value, str) == True:
            value = signals[value]
        else:
            value = int_signals[value]
    elif key == "stdout":
        if os.path.exists(os.path.dirname(value)):
            open(value, "w")
            os.chmod(value, int(calculate_file_rights(process_dict.umask), 8))
            if os.access(value, os.W_OK):
                pass
            else:
                return ("error: stdout file write rights issues")
        else:
            return ("error: stdout file does not exist")
    elif key == "stderr":
        if os.path.exists(os.path.dirname(value)):
            open(value, "w")
            os.chmod(value, int(calculate_file_rights(process_dict.umask), 8))    
            if os.access(value, os.W_OK):
                pass
            else:
                return ("error: stderr file write rights issues")
        else:
            return ("error: stderr file does not exist")
    setattr(process_dict, key, value)
    return (None)


def parse_file(configs, client_socket):
    process_dict = {}
    for glob, programs in configs.items():
        if isinstance(programs, dict) and glob == "programs":
            for proc_name, conf in programs.items():
                if isinstance(conf, dict):
                    error_flag = check_string(str(proc_name))
                    if error_flag != None:
                        print(error_flag)
                        error["error"] = "process name" +  error_flag
                        return (error)
                    elif proc_name.startswith("-"):
                        print("Wrong process name, cannot start with a '-'")
                        error["error"] = "Wrong process name, cannot start with a '-'"
                        return (error)
                    else:
                        process_dict[str(proc_name)] = process_data(str(proc_name))
                        setattr(process_dict[str(proc_name)], "client", client_socket)
                        for key, value in conf.items():
                            try:
                                conf_list.index(key)
                            except ValueError:
                                print("Invalid configuration option")
                                error["error"] = "Invalid configuration option"
                                return (error)
                            error_type = check_value_types(key, value)
                            if error_type != None:
                                print(error_type)
                                error["error"] = error_type
                                return (error)
                            else:
                                error_type = set_attribute(process_dict[str(proc_name)], key, value)
                                if error_type != None:
                                    print(error_type)
                                    error["error"] = error_type
                                    return (error)
                    if process_dict[str(proc_name)].cmd == None:
                        print("cmd configuration mandatory")
                        error["error"] = "cmd configuration mandatory"
                        return (error)
                    if process_dict[str(proc_name)].stdout == process_dict[str(proc_name)].stderr:
                        print("stdout and stderr should be different")
                        error["error"] = "stdout and stderr should be different"
                        return (error)
                else:
                    print("Wrong process section or process section is NULL")
                    error["error"] = "Wrong process section or process section is NULL"
                    return (error)
        else:
            print("File doesn't start with the programs section or programs section is NULL")
            error["error"] = "File doesn't start with the programs section or programs section is NULL"
            return (error)
    return (process_dict)
        

def open_file(conf_file, client_socket):
    print("in open file : ", conf_file)
    try:
        with open(conf_file, 'r') as f:
            try:
                configs = yaml.safe_load(f)
            except:
                print("Invalid yaml")
                error["error"] = "Invalid yaml"
                return (error)
    except FileNotFoundError:
        print("open File not found")
        error["error"] = "File not found"
        return (error)
    except IOError:
        print("Could not read file")
        error["error"] = "Could not read file"
        return (error)
    except PermissionError:
        print("You don't have the permissions to read the file")
        error["error"] = "You don't have the permissions to read the file"
        return (error)
    return parse_file(configs, client_socket)


def main(conf_file, client_socket):
    return open_file(conf_file, client_socket)

#if __name__ == "__main__":
#    if len(sys.argv) != 3:
#        print("Wrong number of arguments")
#        exit(1)
#    main(sys.argv[1], sys.argv[2])

