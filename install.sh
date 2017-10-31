#!/bin/bash
sudo yum install python36
yum install python-pip

#test -d '/etc/init.d' || mkdir -p '/etc/init.d'

mkdir deploy
cd deploy
wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.8.tar.gz
tar xzvf virtualenv-1.8.tar.gz

python virtualenv-1.8/virtualenv.py $HOME/env
python virtualenv-1.8/virtualenv.py ./virtualenv

virtualenv pyenv

. ./pyenv/bin/activate


pip install -r requirements.txt

