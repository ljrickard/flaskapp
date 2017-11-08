#!/bin/bash
yum -y install python36
wget -O virtualenv-15.1.0.tar.gz https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz
tar xzvf virtualenv-15.1.0.tar.gz
python36 virtualenv-15.1.0/virtualenv.py /home/ec2-user/deploy/virtual_env
. /home/ec2-user/deploy/virtual_env/bin/pip install /home/ec2-user/deploy/requirements.txt
#pip install -r 