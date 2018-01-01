#!/bin/bash
set -euo pipefail
/home/ubuntu/deploy/flaskapp/virtual_env/bin/gunicorn \
 	--chdir /home/ubuntu/deploy/flaskapp \
 	--pid /home/ubuntu/deploy/flaskapp/gunicorn.pid \
 	--config /home/ubuntu/deploy/flaskapp/gunicorn.py app:app


/home/ubuntu/deploy/flaskapp/virtual_env/bin/celery multi start w1 w2 w3 w4 w5 w6 \
    --app=app.celery \
    --pidfile="/home/ubuntu/deploy/flaskapp/%n.pid" \
    --workdir="/home/ubuntu/deploy/flaskapp"
    # -Ofair
    #--logfile="/home/ubuntu/deploy/flaskapp/logs/celery/%n.log" \

systemctl daemon-reload
systemctl start flower
systemctl status flower

#/home/ubuntu/deploy/flaskapp/virtual_env/bin/celery worker \
#	--app=app.celery \
#    --pidfile="/home/ubuntu/deploy/flaskapp/%n.pid" \
#    --logfile="/home/ubuntu/deploy/flaskapp/logs/celery/%n.log" \
#    --workdir="/home/ubuntu/deploy/flaskapp" flower
