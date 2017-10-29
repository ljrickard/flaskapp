#!/bin/bash
sudo yum install python36
yum install python-pip

test -d '/etc/init.d' || mkdir -p '/etc/init.d'
