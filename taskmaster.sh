#!/bin/bash

nohup python3 server.py $1 &
python3 cli.py
