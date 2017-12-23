#!/bin/bash
set -euo pipefail
/home/ec2-user/deploy/virtual_env/bin/gunicorn --chdir /home/ec2-user/deploy -p /home/ec2-user/deploy/gunicorn.pid -c /home/ec2-user/deploy/gunicorn.py app:app


/home/ec2-user/deploy/virtual_env/bin/celery multi start c1 c2 c3 c4 \
    --app app.celery \
    --pidfile="/home/ec2-user/deploy/c_%.pid" \
    --logfile="/home/ec2-user/deploy/logs/celery/%n%I.log" \
    --workdir="/home/ec2-user/deploy"

