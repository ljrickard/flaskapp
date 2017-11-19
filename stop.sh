#!/bin/bash
set -euo pipefail
VALUE=${"/home/ec2-user/deploy/GFILE":-}
if [ ! -f VALUE ];
then
	echo "No pid found. No application to stop"
else
	pid=$(cat /home/ec2-user/deploy/GFILE)
	echo "Sending TERM signal to $pid"
	exec kill -s TERM $pid
fi
