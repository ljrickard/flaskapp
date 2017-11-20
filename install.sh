#!/bin/bash
set -euo pipefail
yum -y install python36
wget -O /home/ec2-user/deploy/virtualenv-15.1.0.tar.gz https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz
tar xzvf /home/ec2-user/deploy/virtualenv-15.1.0.tar.gz -C /home/ec2-user/deploy/
python36 /home/ec2-user/deploy/virtualenv-15.1.0/virtualenv.py /home/ec2-user/deploy/virtual_env
/home/ec2-user/deploy/virtual_env/bin/pip install -r /home/ec2-user/deploy/requirements.txt