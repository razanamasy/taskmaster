#!/bin/bash

if [ $# -eq 0 ]; then
    >&2 echo "you need to provide path file"
    exit 1
fi

nohup python3 server/server.py $1 $2 $3 &

sleep 2

python3 client/cli.py $2 $3
