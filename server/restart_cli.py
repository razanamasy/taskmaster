from start_launch import main as main_starting

def main(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list):
    #gestion erreur fonction
	#Voir aussi le dernier exit code pour savoir si ca a ete stop gracefully
    if process.fatal == False:
		#Check si c'est en backlog --> si oui rien faire (END)
		#SI ca run PAS --> (et donc pas en backlog)
			#Si stop gracefully ne rien faire (END)
			#Si fatal
				#Enlever fatal et restart a la main
			#Si crash  apres run mais pas auto restart (Gracefully deja ecarte)
				#restart a la main
		#SI ca run 
			#Si auto restart
				#Kill puis rien faire car autorestart
			#Sinon (Pas autorestart)
				#kill gracefully
				#main_starting a la main
        main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
    else:
        process.fatal == False
        main_starting(client_proc_dict, fd, key, running_table, mutex_proc_dict, thread_list)
