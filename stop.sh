#!/bin/bash
set -euo pipefail

/home/ec2-user/deploy/virtual_env/bin/celery multi stopwait w1 \
	--pidfile="/home/ec2-user/deploy/w1.pid"
/home/ec2-user/deploy/virtual_env/bin/celery multi stopwait w2 \
	--pidfile="/home/ec2-user/deploy/w2.pid"
/home/ec2-user/deploy/virtual_env/bin/celery multi stopwait w3 \
	--pidfile="/home/ec2-user/deploy/w3.pid"
/home/ec2-user/deploy/virtual_env/bin/celery multi stopwait w4 \
	--pidfile="/home/ec2-user/deploy/w4.pid"
/home/ec2-user/deploy/virtual_env/bin/celery multi stopwait w5 \
 	--pidfile="/home/ec2-user/deploy/w5.pid"
/home/ec2-user/deploy/virtual_env/bin/celery multi stopwait w6 \
	--pidfile="/home/ec2-user/deploy/w6.pid"

gunicorn_pid="/home/ec2-user/deploy/gunicorn.pid"

if [ -e $gunicorn_pid ]; then
	pid=$(cat $gunicorn_pid)
	echo "Sending TERM signal to $pid"
	exec kill -s TERM $pid
else
	echo "No pid file found"
fi
