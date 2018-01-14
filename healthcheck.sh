#!/bin/bash
http_status=$(curl -sL -w "%{http_code}" "0.0.0.0:8000/healthcheck" -o /dev/null)
if [ $http_status = "200" ]; then
   	echo "Endpoint point started successfully"
else
	echo "Endpoint failed to start"
	exit 1
fi


# check each service with -> systemctl is-failed application.service