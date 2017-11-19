#!/bin/bash

VIRTUAL_ENV_DIRECTORY='/home/ec2-user/deploy/virtual_env'
PY_CACHE_DIRECTORY='/home/ec2-user/deploy/__pycache__'

if [ -d $VIRTUAL_ENV_DIRECTORY ]; then
  	echo 'removing virtual_env'
	rm -rf $VIRTUAL_ENV_DIRECTORY
fi

if [ -d $PY_CACHE_DIRECTORY ]; then
	echo 'removing __pycache__'
  	rm -rf $PY_CACHE_DIRECTORY
fi
