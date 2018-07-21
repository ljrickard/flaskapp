pid='/run/gunicorn/pid'
bind='unix:/run/gunicorn/socket'
chdir='/home/ubuntu/deploy/flaskapp/'
workers=4
worker_class='sync'
worker_connections=1000
timeout=30
user=None
loglevel='debug'
accesslog='/home/ubuntu/deploy/flaskapp/logs/gunicorn/gunicorn-access.log'
access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'