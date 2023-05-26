#!/bin/bash

if [ $# -ne 2 ]; then
	>&2 echo "command format : bash start_server CONF_FILE PORT"
	echo "(local connexion)"
    exit 1
fi

rm -rf /tmp/taskmaster.log
file_path="/tmp/taskmaster.log"

PYTHONUNBUFFERED=1 nohup python3 server/server.py $1 $2 $3 >> $file_path & 


sleep 2

bash start_client.sh $2
