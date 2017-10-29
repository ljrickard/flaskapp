#!/bin/bash

#exec gunicorn -p gunicorn.pid -c ./gunicorn.py app:app
      
initd_directory='/etc/init.d'

echo "Starting app as `whoami`"

cp celeryd /etc/init.d


#celery -A app.celery worker --loglevel=info &

exec chmod 755 /etc/init.d/celeryd
exec chown root: /etc/init.d/celeryd
exec /etc/init.d/celeryd start
