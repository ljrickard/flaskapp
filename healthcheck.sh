#!/bin/bash
http_status=$(curl -sL -w --unix-socket /run/gunicorn/socket "%{http_code}" "http:/healthcheck" -o /dev/null)
if [ $http_status = "200" ]; then
   	echo "Endpoint point started successfully"
else
	echo "Endpoint failed to start"
	exit 1
fi


# check each service with -> systemctl is-failed application.service