#!/bin/bash
set -euo pipefail
VIRTUAL_ENV_DIRECTORY='/home/ubuntu/deploy/virtual_env'
VIRTUAL_ENV_PACKAGE='/home/ubuntu/deploy/virtualenv-15.1.0'
VIRTUAL_ENV_TAR='/home/ubuntu/deploy/virtualenv-15.1.0.tar.gz'
PY_CACHE_DIRECTORY='/home/ubuntu/deploy/__pycache__'

if [ -d $VIRTUAL_ENV_DIRECTORY ]; then
  	echo 'removing virtual_env'
	rm -rf $VIRTUAL_ENV_DIRECTORY
fi

if [ -d $VIRTUAL_ENV_PACKAGE ]; then
  	echo 'removing virtual_env package'
	rm -rf $VIRTUAL_ENV_PACKAGE
fi

if [ -d $VIRTUAL_ENV_TAR ]; then
  	echo 'removing virtual_env tar'
	rm -rf $VIRTUAL_ENV_TAR
fi

if [ -d $PY_CACHE_DIRECTORY ]; then
	echo 'removing __pycache__'
  	rm -rf $PY_CACHE_DIRECTORY
fi