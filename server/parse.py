import yaml
import sys
import os
from process_struct import *
from parse_utils import *
from timestamp import *

error = {}
conf_list = ["cmd", "numprocs", "umask", "workingdir", "autostart", "autorestart", "exitcodes", "startretries", "starttime", "stopsignal", "stoptime", "stdout", "stderr", "env"]
int_signals = {15: "TERM", 1: "HUP", 2: "INT", 3: "QUIT", 9: "KILL", 10: "USR1", 12: "USR2"}

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
        if isinstance(value, int) == True:
            value = int_signals[value]
    elif key == "stdout":
        if os.path.exists(os.path.dirname(value)):
            file = open(value, "w")
            os.chmod(value, int(calculate_file_rights(process_dict.umask), 8))
            if os.access(value, os.W_OK):
                pass
            else:
                file.close()
                return ("error: stdout file write rights issues")
            file.close()
        else:
            return ("error: stdout file does not exist")
    elif key == "stderr":
        if os.path.exists(os.path.dirname(value)):
            file = open(value, "w")
            os.chmod(value, int(calculate_file_rights(process_dict.umask), 8))    
            if os.access(value, os.W_OK):
                pass
            else:
                file.close()
                return ("error: stderr file write rights issues")
            file.close()
        else:
            return ("error: stderr file does not exist")
    setattr(process_dict, key, value)
    return (None)


def parse_file(configs):
    process_dict = {}
    for glob, programs in configs.items():
        if isinstance(programs, dict) and glob == "programs":
            for proc_name, conf in programs.items():
                if isinstance(conf, dict):
                    error_flag = check_string(str(proc_name))
                    if error_flag != None:
                        print(timestamp('CRIT') + error_flag + "\n", end="", flush=True)
                        error["error"] = "process name" +  error_flag
                        return (error)
                    elif "-" in str(proc_name):
                        print(timestamp('CRIT') + "Wrong process name, cannot contain a '-'\n", end="", flush=True)
                        error["error"] = "Wrong process name, cannot contain a '-'"
                        return (error)
                    else:
                        process_dict[str(proc_name)] = process_data(str(proc_name))
                        for key, value in conf.items():
                            try:
                                conf_list.index(key)
                            except ValueError:
                                print(timestamp('CRIT') + "Invalid configuration option\n", end="", flush=True)
                                error["error"] = "Invalid configuration option"
                                return (error)
                            error_type = check_value_types(key, value)
                            if error_type != None:
                                print(timestamp('CRIT') + error_type + "\n", end="", flush=True)
                                error["error"] = error_type
                                return (error)
                            else:
                                error_type = set_attribute(process_dict[str(proc_name)], key, value)
                                if error_type != None:
                                    print(timestamp('CRIT') + error_type + "\n", end="", flush=True)
                                    error["error"] = error_type
                                    return (error)
                    if process_dict[str(proc_name)].cmd == None:
                        print(timestamp('CRIT') + "cmd configuration mandatory\n", end="", flush=True)
                        error["error"] = "cmd configuration mandatory"
                        return (error)
                    if process_dict[str(proc_name)].stdout == process_dict[str(proc_name)].stderr:
                        print(timestamp('CRIT') + "stdout and stderr should be different\n", end="", flush=True)
                        error["error"] = "stdout and stderr should be different"
                        return (error)
                    try:
                        os.makedirs(os.path.dirname(process_dict[str(proc_name)].stdout), exist_ok=True)
                        os.makedirs(os.path.dirname(process_dict[str(proc_name)].stderr), exist_ok=True)
                    except Exception as e:
                        print(timestamp('CRIT') + str(e) + "\n", end="", flush=True)
                        error["error"] = str(e)
                        return (error)
                    try:
                        stdout_file = open(process_dict[str(proc_name)].stdout, "x")
                        stderr_file = open(process_dict[str(proc_name)].stderr, "x")
                        stdout_file.close()
                        stderr_file.close()
                    except Exception as e:
                        pass
                    stdout_file = open(process_dict[str(proc_name)].stdout, "w")
                    os.chmod(process_dict[str(proc_name)].stdout, int(calculate_file_rights(process_dict[str(proc_name)].umask), 8))    
                    if os.access(process_dict[str(proc_name)].stdout, os.W_OK):
                        stderr_file = open(process_dict[str(proc_name)].stderr, "w")
                        os.chmod(process_dict[str(proc_name)].stderr, int(calculate_file_rights(process_dict[str(proc_name)].umask), 8))
                        stderr_file.close()
                        stdout_file.close()
                    else:
                        print(timestamp('CRIT') + "stdout and stderr file write rights issues\n", end="", flush=True)
                        error["error"] = "stdout and stderr file write rights issues"
                        stdout_file.close()
                        return (error)
                else:
                    print(timestamp('CRIT') + "Wrong process section or process section is NULL\n", end="", flush=True)
                    error["error"] = "Wrong process section or process section is NULL"
                    return (error)
        else:
            print(timestamp('CRIT') + "File doesn't start with the programs section or programs section is NULL\n", end="", flush=True)
            error["error"] = "File doesn't start with the programs section or programs section is NULL"
            return (error)
    return (process_dict)
        

def open_file(conf_file):
    print(timestamp('INFO') + f"in open file : {conf_file} \n", end="", flush=True)
    try:
        with open(conf_file, 'r') as f:
            try:
                configs = yaml.safe_load(f)
            except:
                print(timestamp('CRIT') + "Invalid yaml\n", end="", flush=True)
                error["error"] = "Invalid yaml"
                f.close()
                return (error)
        f.close()
    except FileNotFoundError:
        print(timestamp('CRIT') + "File not foun\n", end="", flush=True)
        error["error"] = "File not found"
        return (error)
    except PermissionError:
        print(timestamp('CRIT') + "You don't have the permissions to read the file\n", end="", flush=True)
        error["error"] = "You don't have the permissions to read the file"
        return (error)
    except IOError:
        print(timestamp('CRIT') + "Could not read file\n", end="", flush=True)
        error["error"] = "Could not read file"
        return (error)
    return parse_file(configs)


def main(conf_file):
    return open_file(conf_file)


