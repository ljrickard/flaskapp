#!/bin/bash
#set -euo pipefail
http_status=$(curl -sL -w "%{http_code}" "localhost:8000/status" -o /dev/null)
if [ $http_status = "200" ]; then
   	echo "Endpoint point running successfully"
else
	echo "Endpoint failed to start"
	exit 1
fi