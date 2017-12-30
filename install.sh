#!/bin/bash
set -euo pipefail
add-apt-repository -y ppa:jonathonf/python-3.6
apt-get -y update
apt-get -y install python3.6
wget -O /home/ubuntu/deploy/flaskapp/virtualenv-15.1.0.tar.gz https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz
tar xzvf /home/ubuntu/deploy/flaskapp/virtualenv-15.1.0.tar.gz -C /home/ubuntu/deploy/flaskapp/
python3.6 /home/ubuntu/deploy/flaskapp/virtualenv-15.1.0/virtualenv.py /home/ubuntu/deploy/flaskapp/virtual_env
/home/ubuntu/deploy/flaskapp/virtual_env/bin/pip install -r /home/ubuntu/deploy/flaskapp/requirements.txt
mkdir -p /home/ubuntu/deploy/flaskapp/logs
mkdir -p /home/ubuntu/deploy/flaskapp/logs/app
mkdir -p /home/ubuntu/deploy/flaskapp/logs/flower
mkdir -p /home/ubuntu/deploy/flaskapp/logs/celery


