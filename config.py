import os

class Config(): pass

class DevelopmentConfig(Config):
    DEBUG=True
    TESTING=True
    REDIS_URI='127.0.0.1'
    REDIS_PORT=6379
    REDIS_DB=3
    LOG_DIR='{0}/logs'.format(os.getcwd())
    REDIS_PASSWORD='foobar'
    CELERY_BROKER='redis://:{0}@{1}:{2}/{3}'.format(REDIS_PASSWORD, REDIS_URI, REDIS_PORT, REDIS_DB)

class ProductionConfig(Config):
    DEBUG=False
    LOG_DIR='/home/ubuntu/deploy/flaskapp/logs'
    REDIS_URI=os.getenv('REDIS_URI', None)
    REDIS_PORT=os.getenv('REDIS_PORT', None)
    REDIS_DB=os.getenv('REDIS_DB', None)
    REDIS_PASSWORD=os.getenv('REDIS_PASSWORD', None)
    CELERY_BROKER='redis://:{0}@{1}:{2}/{3}'.format(REDIS_PASSWORD, REDIS_URI, REDIS_PORT, REDIS_DB)
