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

# setup awslogs
#wget -O /home/ubuntu/deploy/flaskapp/awslogs-agent-setup.py https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py
#chmod +x /home/ubuntu/deploy/flaskapp/awslogs-agent-setup.py
#python3 /home/ubuntu/deploy/flaskapp/awslogs-agent-setup.py -n -r us-east-1 -c s3://aws-codedeploy-us-east-1/cloudwatch/awslogs.conf
#mkdir -p /var/awslogs/etc/config
#cp codedeploy_logs.conf /var/awslogs/etc/config/
#service awslogs restart

