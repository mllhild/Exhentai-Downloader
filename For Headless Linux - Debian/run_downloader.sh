#!/bin/bash
nohup python3 downloadScript.py 2>&1 | ts '[%Y-%m-%d %H:%M:%S]' > download.log &
echo "Downloader started in background. Logging to download.log"
