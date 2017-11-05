#!/bin/bash

echo "Installing virtualenv as `whoami`"

yum -y install python36
wget -O virtualenv-15.1.0.tar.gz https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz
tar xzvf virtualenv-15.1.0.tar.gz
#cp -a virtualenv-15.1.0 /home/ec2-user/deploy

#python virtualenv-15.1.0/virtualenv.py ./virtualenv

python36 virtualenv-15.1.0/virtualenv.py /home/ec2-user/deploy/virtual_env

#virtualenv pyenv

#. ./pyenv/bin/activate


#pip install -r requirements.txt

