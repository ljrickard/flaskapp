#!/bin/bash

echo "Enviroment details"
echo
echo "HOME DIR is $HOME"
echo
echo "PATH DIR is $PATH"
echo
echo "USER DIR is $USER"
echo

echo "Stopping app as `whoami`"

#. ./pyenv/bin/activate

#pid=$(cat gunicorn.pid)

#if [ -z "$pid" ]
#then
#      echo "No pid found. No application to stop"
#else
#      echo "Sending TERM signal to $pid"
#      exec kill -s TERM $pid
#fi
