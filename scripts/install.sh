#!/bin/bash

echo "Installing virtualenv as `whoami`"

wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.8.tar.gz
tar xzvf virtualenv-1.8.tar.gz
cp -a virtualenv-1.8 /home/ec2-user/deploy
#python virtualenv-1.8/virtualenv.py ./virtualenv

#virtualenv pyenv

#. ./pyenv/bin/activate


#pip install -r requirements.txt

