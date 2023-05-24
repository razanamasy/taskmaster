#!/bin/bash

if [ $# -ne 2 ]; then
	>&2 echo "command format : bash start_server CONF_FILE PORT"
	echo "(local connexion)"
    exit 1
fi

file_path="/tmp/taskmaster.log"
#if [ -f "$file_path" ];then
#    rm "$file_path"
#fi


#nohup python3 server/server.py $1 $2 $3 &> $file_path #error ok but not if it work
nohup python3 server/server.py $1 $2 $3 > $file_path & #Ok if it work but don't catch server i dunno why need to catch error from client if error 

#cat "$file_path"

#if cat "$file_path" | grep "Server error"
#then
#    cat "$file_path"
#    exit 1
#fi

sleep 2

bash start_client.sh $2
