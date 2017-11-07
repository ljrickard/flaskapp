#!/bin/bash
DIRECTORY='/home/ec2-user/deploy/virtual_env'
if [ -d $DIRECTORY ]; then
  rm -rf $DIRECTORY
fi
