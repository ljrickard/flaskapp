import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask import current_app as app


class Config(object):
    formatter = logging.Formatter(
        "%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s")
    handler = TimedRotatingFileHandler(
        'logs/{0}-{1}.log'.format(str(datetime.now()), os.getpid()), when='H', interval=1)
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
    RAILS_URI = os.getenv('RAILS_URI', '')
    RAILS_PORT = os.getenv('RAILS_PORT', '')
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    REDIS_URI = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 3
    RAILS_URI = 'http://127.0.0.1'
    RAILS_PORT = 3000
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
