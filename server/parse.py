import yaml
import sys
from process_struct import *
from parse_utils import *

error = {}
conf_list = ["cmd", "numprocs", "umask", "workingdir", "autostart", "autorestart", "exitcodes", "startretries", "starttime", "stopsignal", "stoptime", "stdout", "stderr", "env"]

def check_value_types(key, value):
    error_flag = None 
    #case "cmd":
    if key == "numprocs":
        error_flag = check_int(value, 1, 10)
        if error_flag != None:
            error_flag = "error: numprocs " + error_flag
            return (error_flag)
    #case "umask":
    #case "workingdir":
    #case "autostart":
    #case "autorestart":
    #case "exitcodes":
    elif key == "startretries":
        error_flag = check_int(value, 0, 50)
        if error_flag != None:
            error_flag = "error: startretries " + error_flag
            return (error_flag)
    elif key == "starttime":
        error_flag = check_int(value, 0, 60)
        if error_flag != None:
            error_flag = "error: startime " + error_flag
            return (error_flag)
    #case "stopsignal":
    elif key == "stoptime":
        error_flag = check_int(value, 0, 60)
        if error_flag != None:
            error_flag = "error: stoptime " + error_flag
            return (error_flag)
    #case "stdout":
    #case "stderr":
    #case "env":
    return (error_flag)

def parse_file(configs, client_socket):
    process_dict = {}
    for glob, programs in configs.items():
        if isinstance(programs, dict) and programs != "programs":
            for proc_name, conf in programs.items():
                if isinstance(conf, dict):
                    process_dict[proc_name] = process_data(proc_name)
                    setattr(process_dict[proc_name], "client", client_socket)
                    for key, value in conf.items():
                        try:
                            conf_list.index(key)
                        except ValueError:
                            print("Invalid configuration option")
                            error["error"] = "Invalid configuration option"
                            return (error)
                        if isinstance(value, dict) and key != "env":
                            print("Wrong configuration value format")
                            error["error"] = "Wrong configuration value format"
                            return (error)
                        else:
                            error_type = check_value_types(key, value)
                            if error_type != None:
                                print(error_type)
                                error["error"] = error_type
                                return (error)
                            else:
                                setattr(process_dict[proc_name], key, value)
                else:
                    print("Wrong process section or process section is NULL")
                    error["error"] = "Wrong process section or process section is NULL"
                    return (error)
        else:
            print("File doesn't start with the programs section or programs section is NULL")
            error["error"] = "File doesn't start with the programs section or programs section is NULL"
            return (error)

    print(process_dict[proc_name])
    return (process_dict)
        

def open_file(conf_file, client_socket):
    print("in open file : ", conf_file)
    try:
        with open(conf_file, 'r') as f:
            try:
                configs = yaml.safe_load(f)
                print(configs)
            except:
                print("Invalid yaml")
                error["error"] = "Invalid yaml"
                return (error)
            return parse_file(configs, client_socket)
    except FileNotFoundError:
        print("File not found")
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

def main(conf_file, client_socket):
    return open_file(conf_file, client_socket)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments")
        exit(1)
    main(sys.argv[1], sys.argv[2])
