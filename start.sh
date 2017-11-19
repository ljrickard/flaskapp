#!/bin/bash
#exec /home/ec2-user/deploy/virtual_env/bin/gunicorn -p GFILE -c /home/ec2-user/deploy/gunicorn.py /home/ec2-user/deploy/app:app


/home/ec2-user/deploy/virtual_env/bin/gunicorn --chdir /home/ec2-user/deploy -p GFILE -c gunicorn app:app

#set -e

#initd_directory='/etc/init.d'

#echo "Starting app as `whoami`"

#cp celeryd /etc/init.d


#celery -A app.celery worker --loglevel=info &

#exec chmod 755 /etc/init.d/celeryd
#exec chown root: /etc/init.d/celeryd
#exec /etc/init.d/celeryd start


#gunicorn -p GFILE -w 4 app:app

#. /home/ec2-user/deploy/virtual_env/bin/activate
#pip install -r /home/ec2-user/deploy/requirements.txt

#gunicorn -w 2 -b 0.0.0.0:8000 --chdir /home/telessaude/telessaude_branch_master telessaude.wsgi_dev:application --reload --timeout 900

