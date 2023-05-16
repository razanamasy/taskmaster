def main(client_proc_dict, fd, key):
    process = client_proc_dict[fd][key]
    if process.backlog == True: #Il faudra preciser avec failure plus tard
        return "Process " + key + " :BACKLOG (need to precise)"
    if process.fatal == True:
        return "Process " + key + " :FATAL"
    if process.stopping == True:
        return "Process " + key + " :STOPPING"
    if process.stopped == True:
        return "Process " + key + " :STOPPED"
    if process.running == True:
        return "Process " + key + " :RUNNING"
