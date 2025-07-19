#!/bin/bash

PID=$(pgrep -f downloadScript.py)

if [ -z "$PID" ]; then
    echo "Script is not running."
else
    echo "Stopping downloadScript.py with PID $PID..."
    kill "$PID"
    echo "Script stopped."
fi
