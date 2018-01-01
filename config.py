import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask import current_app
import os

class Config(): pass

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    REDIS_URI = 'redis://localhost'
    REDIS_PORT = 6379
    REDIS_DB = 3
    LOG_DIR = '{0}/logs'.format(os.getcwd())
    FLOWERS_API = 'http://localhost:5555/api'
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'

class ProductionConfig(Config):
    DEBUG = False
    REDIS_URI = os.getenv('REDIS_URI', 'redis://ec2-54-175-79-8.compute-1.amazonaws.com')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', 3)
    LOG_DIR = '/home/ubuntu/deploy/flaskapp/logs/app'
    FLOWERS_API = 'http://0.0.0.0:5555/api'    
    CELERY_BROKER_URL = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
    CELERY_RESULT_BACKEND = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
