#!/bin/bash
set -euo pipefail

if [ -e "/home/ubuntu/deploy/w1.pid" ]; then
	/home/ubuntu/deploy/virtual_env/bin/celery multi stopwait w1 \
		--pidfile="/home/ubuntu/deploy/w1.pid"
fi

if [ -e "/home/ubuntu/deploy/w2.pid" ]; then
	/home/ubuntu/deploy/virtual_env/bin/celery multi stopwait w2 \
		--pidfile="/home/ubuntu/deploy/w2.pid"
fi

if [ -e "/home/ubuntu/deploy/w3.pid" ]; then
	/home/ubuntu/deploy/virtual_env/bin/celery multi stopwait w3 \
		--pidfile="/home/ubuntu/deploy/w3.pid"
fi

if [ -e "/home/ubuntu/deploy/w4.pid" ]; then
	/home/ubuntu/deploy/virtual_env/bin/celery multi stopwait w4 \
		--pidfile="/home/ubuntu/deploy/w4.pid"
fi

if [ -e "/home/ubuntu/deploy/w5.pid" ]; then
	/home/ubuntu/deploy/virtual_env/bin/celery multi stopwait w5 \
		--pidfile="/home/ubuntu/deploy/w5.pid"
fi

if [ -e "/home/ubuntu/deploy/w6.pid" ]; then
	/home/ubuntu/deploy/virtual_env/bin/celery multi stopwait w6 \
		--pidfile="/home/ubuntu/deploy/w6.pid"
fi

gunicorn_pid="/home/ubuntu/deploy/gunicorn.pid"

if [ -e $gunicorn_pid ]; then
	pid=$(cat $gunicorn_pid)
	echo "Sending TERM signal to $pid"
	exec kill -s TERM $pid
else
	echo "No pid file found"
fi
