#!/bin/bash
set -euo pipefail

#/home/ubuntu/deploy/flaskapp/virtual_env/bin/celery multi start w1 w2 w3 w4 w5 w6 \
#    --app=app.celery \
#    --pidfile="/home/ubuntu/deploy/flaskapp/%n.pid" \
#    --logfile="/home/ubuntu/deploy/flaskapp/logs/app/%n.log" \
#    --workdir="/home/ubuntu/deploy/flaskapp"
    # -Ofair

#systemctl daemon-reload
#systemctl start flower
#systemctl status flower

systemctl daemon-reload
systemctl enable gunicorn.socket
systemctl start gunicorn.socket

systemctl enable gunicorn.service
systemctl start gunicorn.service


systemctl enable celery.service
systemctl start celery.service
        