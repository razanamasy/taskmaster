#!/bin/bash

if [ $# -ne 3 ]; then
    >&2 echo "command format : bash start_server CONF_FILE IP PORT"
    exit 1
fi

nohup python3 server/server.py $1 $2 $3 &> /tmp/nohup.out

file_path="/tmp/nohup.out"

if cat /tmp/nohup.out | grep -q "BAD IP OR PORT"; then
    cat /tmp/nohup.out
    rm /tmp/nohup.out
    exit 1
fi

sleep 2

python3 client/cli.py $2 $3
