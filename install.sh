#!/bin/bash
set -euo pipefail
apt -y install python36
wget -O /home/ubuntu/deploy/virtualenv-15.1.0.tar.gz https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz
tar xzvf /home/ubuntu/deploy/virtualenv-15.1.0.tar.gz -C /home/ubuntu/deploy/
python36 /home/ubuntu/deploy/virtualenv-15.1.0/virtualenv.py /home/ubuntu/deploy/virtual_env
/home/ubuntu/deploy/virtual_env/bin/pip install -r /home/ubuntu/deploy/requirements.txt