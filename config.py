import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask import current_app as app


class Config(object):
    formatter = logging.Formatter(
        "%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s")
    handler = TimedRotatingFileHandler(
        '/var/log/flaskapp/{0}-{1}.log'.format(str(datetime.now()), os.getpid()), when='H', interval=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)


class ProductionConfig(Config):
    DEBUG = False
    REDIS_URI = os.getenv('REDIS_URI', '')
    REDIS_PORT = os.getenv('REDIS_PORT', '')
    REDIS_DB = os.getenv('REDIS_DB', '')
    CELERY_BROKER_URL = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
    CELERY_RESULT_BACKEND = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    REDIS_URI = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 3
    CELERY_BROKER_URL = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
    CELERY_RESULT_BACKEND = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
    #CELERY_BROKER_URL = 'redis://localhost:6379'
    #CELERY_RESULT_BACKEND = 'redis://localhost:6379'
