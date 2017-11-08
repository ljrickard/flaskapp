#!/bin/bash
VIRTUAL_ENV_DIRECTORY='/home/ec2-user/deploy/virtual_env'
PY_CACHE_DIRECTORY='/home/ec2-user/deploy/__pycache__'

if [ -d $DIRECTORY ]; then
  rm -rf $DIRECTORY
fi

if [ -d $PY_CACHE_DIRECTORY ]; then
  rm -rf $PY_CACHE_DIRECTORY
fi
