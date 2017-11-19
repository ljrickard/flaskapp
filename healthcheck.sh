#!/bin/bash
if curl -sL -w "%{http_code}\\n" "localhost:8000/status" -o /dev/null
	then 
		echo "Endpoint point running successfully"
	else
		echo "Endpoint failed to start"
		exit 1
fi