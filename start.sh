#!/bin/bash

echo "Enviroment details"
echo
echo "HOME DIR is $HOME"
echo
echo "PATH DIR is $PATH"
echo
echo "USER DIR is $USER"
echo

echo "Stopping app as `whoami`"

#. ./pyenv/bin/activate

#exec gunicorn -p gunicorn.pid -c ./gunicorn.py app:app
     
#set -e

#initd_directory='/etc/init.d'

#echo "Starting app as `whoami`"

#cp celeryd /etc/init.d


#celery -A app.celery worker --loglevel=info &

#exec chmod 755 /etc/init.d/celeryd
#exec chown root: /etc/init.d/celeryd
#exec /etc/init.d/celeryd start
