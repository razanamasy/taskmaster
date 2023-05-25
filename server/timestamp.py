from datetime import datetime

def timestamp(status):
    from datetime import datetime

	# datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S, " + status + " ")
    return (dt_string)