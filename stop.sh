#!/bin/bash

echo "Stopping as `whoami`"

#. ./pyenv/bin/activate

#pid=$(cat gunicorn.pid)

#if [ -z "$pid" ]
#then
#      echo "No pid found. No application to stop"
#else
#      echo "Sending TERM signal to $pid"
#      exec kill -s TERM $pid
#fi
