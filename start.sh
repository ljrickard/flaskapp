#!/bin/bash
set -euo pipefail
/home/ubuntu/deploy/virtual_env/bin/gunicorn \
 	--chdir /home/ubuntu/deploy \
 	--pid /home/ubuntu/deploy/gunicorn.pid \
 	--config /home/ubuntu/deploy/gunicorn.py app:app


/home/ubuntu/deploy/virtual_env/bin/celery multi start w1 w2 w3 w4 w5 w6 \
    --app=app.celery \
    --pidfile="/home/ubuntu/deploy/%n.pid" \
    --logfile="/home/ubuntu/deploy/logs/celery/%n.log" \
    --workdir="/home/ubuntu/deploy"
    # -Ofair

/home/ubuntu/deploy/virtual_env/bin/celery worker \
	--app=app.celery \
    --pidfile="/home/ubuntu/deploy/%n.pid" \
    --logfile="/home/ubuntu/deploy/logs/celery/%n.log" \
    --workdir="/home/ubuntu/deploy" flower
