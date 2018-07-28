#!/bin/bash
systemctl stop gunicorn.socket
systemctl stop gunicorn.service
systemctl stop celery.service