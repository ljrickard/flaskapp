#!/bin/bash
set -euo pipefail

systemctl daemon-reload
systemctl enable gunicorn.socket
systemctl start gunicorn.socket

systemctl enable gunicorn.service
systemctl start gunicorn.service


systemctl enable celery.service
systemctl start celery.service
        
service awslogs start