#!/bin/bash
set -euo pipefail
GFILE="/home/ec2-user/deploy/gunicorn.pid"

if [ -e $GFILE ]; then
	pid=$(cat $GFILE)
	echo "Sending TERM signal to $pid"
	exec kill -s TERM $pid
else
	echo "No pid file found"
fi