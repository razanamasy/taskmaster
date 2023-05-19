import calendar
import time

def main(list_proc_data, key, mutex_proc_dict):
    process = list_proc_data[key]
    print(f"MY PROCESS STATUS IS : {process}")
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.backlog[0] == True: #Il faudra preciser avec failure plus tard
        print(f"B_S ===== {process.backoff_starting}")
        delay = time_stamp - process.backlog[1]
        if process.backoff_starting[0] == True:
            return "Process " + key + " :STARTING since :" + str(delay) + " seconds"
        elif process.backoff_starting[0] == False:
            return "Process " + key + " :BACKOFF since :" + str(delay) + " seconds"
    if process.fatal[0] == True:
        delay = time_stamp - process.fatal[1]
        return "Process " + key + " :FATAL since:" + str(delay) + " seconds"
    if process.stopping[0] == True:
        delay = time_stamp - process.stopping[1]
        return "Process " + key + " :STOPPING since:" + str(delay) + " seconds"
    if process.running[0] == True:
        delay = time_stamp - process.running[1]
        return "Process " + key + " :RUNNING since:" + str(delay) + " seconds"
    if process.stopped[0] == True:
        delay = time_stamp - process.stopped[1]
        return "Process " + key + " :STOPPED since:" + str(delay) + " seconds"
    print("NoNe case here fuck off")
