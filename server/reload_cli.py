from start_launch import main as main_starting

def compare_and_replace(new_process, old_process):
	to_reload = False


	

def manage_process(new_process, old_process, key):
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
	if new_process.cmd != old_process.cmd:
		old_process.cmd = new_process.cmd
		to_reload = True
	return to_reload

def main(new_list, client_proc_dict, fd):
	old_list = client_proc_dict[fd]
	#check the changes in new list
	for process in new_list:
		if process in old_list:
			if manage_process(new_list[process], old_list, process) == True:
				#Need to check the status of process before : 
				#Backlog wait 
				#Stopping ???
				#stopped ? depend on autostart we launch it
                main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
				#RELOAD HERE
