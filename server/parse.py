import yaml
import sys
from process_struct import *

def parse_file(configs):
    process_dict = {}
    if "programs" in configs == False:
        print("No programs section")
        exit(1)
    else:
        for glob, programs in configs.items():
            if isinstance(programs, dict) and programs != "programs":
                for proc_name, conf in programs.items():
                    if isinstance(conf, dict):
                        process_dict[proc_name] = process_data(proc_name)
                        for key, value in conf.items():
                            if isinstance(value, dict):
                                print("Wrong config file3")
                                exit(1)
                            else:
                                setattr(process_dict[proc_name], key, value)
                    else:
                        print("Wrong config file2")
                        exit(1)
            else:
                print("Wrong config file1")
                exit(1)
    print(process_dict);
        

def open_file(conf_file):
    try:
        with open(conf_file, 'r') as f:
            configs = yaml.safe_load(f)
            parse_file(configs)
    except FileNotFoundError:
        print("File not found")
        exit(1)
    except IOError:
        print("Could not read file")
        exit(1)
    except PermissionError:
        print("You don't have the permissions to read the file")
        exit(1)

def main(arg1):
    open_file(arg1);

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        exit(1)
    main(sys.argv[1])

