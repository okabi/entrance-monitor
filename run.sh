#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Error: please input mjpg-streamer's uri."
    echo "Usage: ${0} stream-uri"
    echo "  stream-uri: ex. http://192.168.0.10:9000/?action=stream"
    exit 1
fi

uri=$1

mkdir -p jpg
nohup python2.7 entrance-monitor.py ${uri} > /dev/null &
echo "Monitor has Started. If you want to stop the monitor, please kill the process manually."
