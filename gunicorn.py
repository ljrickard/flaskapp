import multiprocessing

#bind = "0.0.0.0:8000"
bind = '127.0.0.1:8000'
workers = 4 #multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
daemon = True
user = None
errorlog = 'debug'
loglevel = 'debug'
accesslog = 'debug'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
