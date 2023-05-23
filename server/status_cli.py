import calendar
import time

def main(list_proc_data, key, mutex_proc_dict):
    process = list_proc_data[key]
  #  print(f"MY PROCESS STATUS IS : {process}")
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.backlog[0] == True: #Il faudra preciser avec failure plus tard
        print(f"B_S ===== {process.backoff_starting}")
        delay = time_stamp - process.backoff_starting[1]
        if process.backoff_starting[0] == True:
            return ("STARTING", str(delay))
        elif process.backoff_starting[0] == False:
            return ("BACKOFF", str(delay))
    elif process.fatal[0] == True:
        delay = time_stamp - process.fatal[1]
        return ("FATAL", str(delay))
    elif process.stopping[0] == True:
        delay = time_stamp - process.stopping[1]
        return ("STOPPING", str(delay))
    elif process.stopped[0] == True:
        delay = time_stamp - process.stopped[1]
        return ("STOPPED", str(delay))
    elif process.exited[0] == True:
        delay = time_stamp - process.stopped[1]
        return ("EXITED", str(delay))
    elif process.running[0] == True:
        delay = time_stamp - process.running[1]
        return ("RUNNING", str(delay))
    else:
        return ("UNKNOWN", 0)
