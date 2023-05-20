from start_launch import main as main_starting
from status_cli import main as status
from stop_cli import main as stop

def manage_process(new_process, old_process):
	to_reload = False
	if new_process.numprocs != old_process.numprocs:
		old_process.numprocs = new_process.numprocs
	if new_process.umask != old_process.umask:
		old_process.umask = new_process.umask
	if new_process.workingdir != old_process.workingdir:
		old_process.workingdir = new_process.workingdir
	if new_process.autostart != old_process.autostart:
		old_process.autostart = new_process.autostart
	if new_process.autorestart != old_process.autorestart:
		old_process.autorestart = new_process.autorestart
	if new_process.exitcode != old_process.exitcode:
		old_process.exitcode = new_process.exitcode
	if new_process.startretries != old_process.startretries:
		old_process.startretries = new_process.startretries
	if new_process.starttime != old_process.starttime:
		old_process.starttime = new_process.starttime
	if new_process.stopsignal != old_process.stopsignal:
		old_process.stopsignal = new_process.stopsignal
	if new_process.stoptime != old_process.stoptime:
		old_process.stoptime = new_process.stoptime
	if new_process.stdout != old_process.stdout:
		old_process.stdout = new_process.stdout
	if new_process.stderr != old_process.stderr:
		old_process.stderr = new_process.stderr
	if new_process.env != old_process.env:
		old_process.env = new_process.env
	if new_process.env != old_process.env:
		old_process.env = new_process.env


	if new_process.cmd != old_process.cmd:
		old_process.cmd = new_process.cmd
		to_reload = True

    if to_reload:
        if new_process.running != old_process.running:
            old_process.running = new_process.running
        if new_process.backlog != old_process.backlog:
            old_process.backlog = new_process.backlog
        if new_process.backoff_starting != old_process.backoff_starting:
            old_process.backoff_starting = new_process.backoff_starting
        if new_process.fatal != old_process.fatal:
            old_process.fatal = new_process.fatal
        if new_process.quitting != old_process.quitting:
            old_process.quitting = new_process.quitting
        if new_process.stopping != old_process.stopping:
            old_process.stopping = new_process.stopping
        if new_process.stopped != old_process.stopped:
            old_process.stopped = new_process.stopped
        if new_process.exited != old_process.exited:
            old_process.exited = new_process.exited
        if new_process.quit_with_stop != old_process.quit_with_stop:
            old_process.quit_with_stop = new_process.quit_with_stop

	return to_reload

def main(new_list, list_proc_data, mutex_proc_dict, clients, running_table, thread_list):
	old_list = list_proc_data
	#check the changes in new list
	for process in new_list:
		if process in old_list:
			if manage_process(new_list[process], old_list[process]) == True:
				stop(list_proc_data, process, clients, running_table, mutex_proc_dict, thread_list)
                main_starting(list_proc_data, process, clients, running_table, mutex_proc_dict)
				#RELOAD HERE

    to_delete = []
	for process in old_list:
		if process not in new_list:
            to.delete.append(process)

    for process in to_delete
        stop(list_proc_data, process, clients, running_table, mutex_proc_dict, thread_list)
        running_table.pop(list_proc_data[process].pid)
        list_proc_data.pop(process)
