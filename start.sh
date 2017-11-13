#!/bin/bash
#exec /home/ec2-user/deploy/virtual_env/bin/gunicorn -p GFILE -c /home/ec2-user/deploy/gunicorn.py /home/ec2-user/deploy/app:app
exec /home/ec2-user/deploy/virtual_env/bin/gunicorn -p GFILE -w 4 --daemon --error-logfile /home/ec2-user/deploy/logs/gunicorn_error /home/ec2-user/deploy/app:/home/ec2-user/deploy/app
     
#set -e

#initd_directory='/etc/init.d'

#echo "Starting app as `whoami`"

#cp celeryd /etc/init.d


#celery -A app.celery worker --loglevel=info &

#exec chmod 755 /etc/init.d/celeryd
#exec chown root: /etc/init.d/celeryd
#exec /etc/init.d/celeryd start


#. /home/ec2-user/deploy/virtual_env/bin/activate
#pip install -r /home/ec2-user/deploy/requirements.txt
