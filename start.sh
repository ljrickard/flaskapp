#!/bin/bash
set -euo pipefail
/home/ec2-user/deploy/virtual_env/bin/gunicorn \
 	--chdir /home/ec2-user/deploy \
 	--pid /home/ec2-user/deploy/gunicorn.pid \
 	--config /home/ec2-user/deploy/gunicorn.py app:app


/home/ec2-user/deploy/virtual_env/bin/celery multi start w1 w2 w3 w4 w5 w6 \
    --app=app.celery \
    --pidfile="/home/ec2-user/deploy/%n.pid" \
    --logfile="/home/ec2-user/deploy/logs/celery/%n%I.log" \
    --workdir="/home/ec2-user/deploy"
    # -Ofair

/home/ec2-user/deploy/virtual_env/bin/celery worker start f1 \
	--app=app.celery flower \
    --pidfile="/home/ec2-user/deploy/%n.pid" \
    --logfile="/home/ec2-user/deploy/logs/celery/%n%I.log" \
    --workdir="/home/ec2-user/deploy"
