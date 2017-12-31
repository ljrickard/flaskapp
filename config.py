import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask import current_app

class Config(): pass

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    FLOWERS_API = 'http://localhost:5555/api'
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'

class ProductionConfig(Config):
    DEBUG = False
    FLOWERS_API = 'http://localhost:5555/api'    
    #REDIS_DB = os.getenv('REDIS_DB', '')
    CELERY_BROKER_URL = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
    CELERY_RESULT_BACKEND = 'redis://ec2-54-175-79-8.compute-1.amazonaws.com:6379'
