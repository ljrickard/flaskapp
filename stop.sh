#!/bin/bash
pid=$(cat /home/ec2-user/deploy/GFILE)
if [ -z "$pid" ]
then
	echo "No pid found. No application to stop"
else
  	echo "Sending TERM signal to $pid"
	exec kill -s TERM $pid
fi
