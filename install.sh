#!/bin/bash
set -euo pipefail
add-apt-repository -y ppa:jonathonf/python-3.6
apt-get -y update
apt-get -y install python3.6
wget -O /home/ubuntu/deploy/virtualenv-15.1.0.tar.gz https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz
tar xzvf /home/ubuntu/deploy/virtualenv-15.1.0.tar.gz -C /home/ubuntu/deploy/
python3.6 /home/ubuntu/deploy/virtualenv-15.1.0/virtualenv.py /home/ubuntu/deploy/virtual_env
/home/ubuntu/deploy/virtual_env/bin/pip install -r /home/ubuntu/deploy/requirements.txt