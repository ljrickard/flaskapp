#!/bin/bash
echo "Starting as `whoami`"
. /home/ec2-user/deploy/virtual_env/bin/activate
exec gunicorn -p gunicorn.pid -c /home/ec2-user/deploy/.py app:app
     
#set -e

#initd_directory='/etc/init.d'

#echo "Starting app as `whoami`"

#cp celeryd /etc/init.d


#celery -A app.celery worker --loglevel=info &

#exec chmod 755 /etc/init.d/celeryd
#exec chown root: /etc/init.d/celeryd
#exec /etc/init.d/celeryd start
