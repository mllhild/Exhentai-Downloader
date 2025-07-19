#!/bin/bash

echo "Checking if downloadScript.py is running..."
PID=$(pgrep -f downloadScript.py)

if [ -z "$PID" ]; then
    echo "Script is not running."
else
    echo "Script is running with PID: $PID"
    echo "Last 10 lines of download.log:"
    tail -n 10 download.log
fi
