import calendar
import time

def main(list_proc_data, key):
    process = list_proc_data[key]
    print(f"my process status is : {process}")
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    if process.backlog[0] == True: #Il faudra preciser avec failure plus tard
        delay = time_stamp - process.backlog[1]
        return "Process " + key + " :BACKLOG (need to precise) since :" + str(delay) + " seconds"
    if process.fatal[0] == True:
        delay = time_stamp - process.fatal[1]
        return "Process " + key + " :FATAL since:" + str(delay) + " seconds"
    if process.stopping[0] == True:
        delay = time_stamp - process.stopping[1]
        return "Process " + key + " :STOPPING since:" + str(delay) + " seconds"
    if process.stopped[0] == True:
        delay = time_stamp - process.stopped[1]
        return "Process " + key + " :STOPPED since:" + str(delay) + " seconds"
    if process.running[0] == True:
        delay = time_stamp - process.running[1]
        return "Process " + key + " :RUNNING since:" + str(delay) + " seconds"
