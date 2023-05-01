import yaml
import sys
from process_struct import *

<<<<<<< HEAD
def parse_file(configs):
=======
def parse_file(configs, client_socket):
>>>>>>> master
    process_dict = {}
    if "programs" in configs == False:
        print("No programs section")
        exit(1)
    else:
        for glob, programs in configs.items():
            if isinstance(programs, dict) and programs != "programs":
                for proc_name, conf in programs.items():
                    if isinstance(conf, dict):
<<<<<<< HEAD
                        process_dict[proc_name] = process(proc_name)
=======
                        print("Proc name in parsing : ", proc_name)
                        process_dict[proc_name] = process_data(proc_name)
>>>>>>> master
                        for key, value in conf.items():
                            if isinstance(value, dict):
                                print("Wrong config file3")
                                exit(1)
                            else:
<<<<<<< HEAD
=======
                                print("key and value : ", "|",key,"| " "|",value,"| ")
>>>>>>> master
                                setattr(process_dict[proc_name], key, value)
                    else:
                        print("Wrong config file2")
                        exit(1)
            else:
                print("Wrong config file1")
                exit(1)
<<<<<<< HEAD
    print(process_dict["ls"]);
    print(process_dict["env"]);
        

def open_file(conf_file):
    try:
        with open(conf_file, 'r') as f:
            configs = yaml.safe_load(f)
            parse_file(configs)
=======
    client_proc_dict = {client_socket: process_dict}
    print(client_proc_dict[client_socket]["while"])
    return (client_proc_dict)
        

def open_file(conf_file, client_socket):
    print("in open file : ", conf_file)
    try:
        with open(conf_file, 'r') as f:
            configs = yaml.safe_load(f)
            return parse_file(configs, client_socket)
>>>>>>> master
    except FileNotFoundError:
        print("File not found")
        exit(1)
    except IOError:
        print("Could not read file")
        exit(1)
    except PermissionError:
        print("You don't have the permissions to read the file")
        exit(1)

<<<<<<< HEAD
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        exit(1)
    open_file(sys.argv[1]);
=======
def main(arg1, arg2):
    return open_file(arg1, arg2);

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments")
        exit(1)
    main(sys.argv[1], sys.argv[2])

>>>>>>> master
