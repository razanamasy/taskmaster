#!/bin/bash

nohup python3 server/server.py &

sleep 2

if [ $# -eq 1 ]; then
	python3 client/cli.py $1
fi
