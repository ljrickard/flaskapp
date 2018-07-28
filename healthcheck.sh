#!/bin/bash
http_status=$(curl --unix-socket /run/gunicorn/socket -sL -w "%{http_code}" "http:/healthcheck" -o /dev/null)
if [ $http_status = "200" ]; then
   	echo "Endpoint point started successfully"
else
	echo "Endpoint failed to start"
	exit 1
fi
