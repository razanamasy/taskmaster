_bool = ["true", "True", "False", "false"]
signals = ["TERM", "SIGTERM", "HUP", "SIGHUP", "INT", "SIGINT", "QUIT", "SIGQUIT", "KILL", "SIGKILL", "USR1", "SIGUSR1", "USR2", "SIGUSR2"]
int_signals = [15, 1, 2, 3, 9, 10, 12]

def check_int(value, min, max):
    if value == None:
        return ("is empty")
    else:
        if isinstance(value, int) == False:
            return ("is not an int")
        else:
            if (value < min or value > max):
                return ("value out of range")
    return (None)

def check_string(value):
    if value == None:
        return ("is empty")
    else:
        if isinstance(value, str) == False:
            return ("is not a string")
        else:
            if value.isprintable() == False:
                return ("not printable character in string")
            elif len(value) == 0:
                return ("is empty")
    return (None)

def check_num(value):
    flag = check_string(value)
    if flag == None and value.isnumeric() == False:
        return ("should contain only numeric values")
    return (flag)

def check_umask(value):
    flag = check_num(value)
    if flag == None:
        if len(value) != 3:
            return ("wrong length")
        else:
            for nb in value:
                if 0 <= int(nb) <= 7:
                    continue
                else:
                    return ("wrong permission value")
    return (flag)

def check_bool(value):
    if value == None:
        return ("is empty")
    else:
        if isinstance(value, bool) == False:
            flag = check_string(value)
            if flag == None:
                try:
                    _bool.index(value)
                except ValueError:
                    return ("is not a bool")
            return (flag)
    return (None)

def check_autorestart(value):
    if value == None:
        return ("is empty")
    else:
        if isinstance(value, bool) == False:
            flag = check_string(value)
            if flag == None:
                try:
                    _bool.index(value)
                except ValueError:
                    if (value != "unexpected"):
                        return ("is not a bool or unexpected")
            return (flag)
    return (None)

def check_exitcodes(_list):
    if _list == None:
        return ("is empty")
    else:
        if isinstance(_list, list) == False:
            return ("wrong format")
        else:
            for value in _list:
                if isinstance(value, int) == False:
                    return ("is not an int")
    return (None)

def check_stopsignal(value):
    flag = check_string(value)
    if flag == None:
        try:
            signals.index(value)
        except ValueError:
            return ("wrong signal")
    else:
        if flag == "is not a string":
            if isinstance(value, int) == False:
                return ("is not a signal")
            else:
                try:
                    int_signals.index(value)
                except ValueError:
                    return ("wrong signal value")
                flag = None
    return (flag)

def check_env(_dict):
    if _dict == None:
        return ("is empty")
    else:
        if isinstance(_dict, dict) == False:
            return ("is not a dict")
        else:
            for key, value in _dict.items():
                flag = check_string(key)
                if flag == None:
                    flag = check_string(value)
                    if flag != None:
                        return ("value " + flag)
                else:
                    return ("key " + flag)
    return (None)

def calculate_file_rights(umask):
    rights = ""
    for nb in umask:
        rights = rights + str(6 - int(nb))
    return(rights)
