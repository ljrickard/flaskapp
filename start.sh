#!/bin/bash
set -euo pipefail
/home/ec2-user/deploy/virtual_env/bin/gunicorn --chdir /home/ec2-user/deploy -p /home/ec2-user/deploy/GFILE -c /home/ec2-user/deploy/gunicorn.py app:app

#/etc/init.d/celery_init start

celery multi start worker1 \
    -A /home/ec2-user/deploy/app.celery \
    --pidfile="/home/ec2-user/deploy/C_FILE.pid" \
    --logfile="/home/ec2-user/deploy/logs/celery/%n%I.log"

#set -e

#initd_directory='/etc/init.d'

#echo "Starting app as `whoami`"

#cp celeryd /etc/init.d

#celery -A app.celery worker --loglevel=info &

#exec chmod 755 /etc/init.d/celeryd
#exec chown root: /etc/init.d/celeryd
#exec /etc/init.d/celeryd start


