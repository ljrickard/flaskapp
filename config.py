import os

class Config(): pass

class DevelopmentConfig(Config):
    DEBUG=True
    TESTING=True
    REDIS_URI='54.85.142.26'
    REDIS_PORT=6379
    REDIS_DB=3
    LOG_DIR='{0}/logs'.format(os.getcwd())
    FLOWERS_API='http://localhost:5555/api'
    REDIS_PASSWORD='0HijQIfIxJfWQ27v4yGsgJdySL9rTxc2wkzgZQRYHVvl6FkL6Hc0wjWB9NecCuXm'
    CELERY_BROKER='redis://:{0}@{1}:{2}/{3}'.format(REDIS_PASSWORD, REDIS_URI, REDIS_PORT, REDIS_DB)

class ProductionConfig(Config):
    DEBUG=False
    LOG_DIR='/home/ubuntu/deploy/flaskapp/logs/app'
    FLOWERS_API='http://0.0.0.0:5555/api' 
    REDIS_URI=os.getenv('REDIS_URI', None)
    REDIS_PORT=os.getenv('REDIS_PORT', None)
    REDIS_DB=os.getenv('REDIS_DB', None)
    REDIS_PASSWORD=os.getenv('REDIS_PASSWORD', None)
    CELERY_BROKER='redis://:{0}@{1}:{2}/{3}'.format(REDIS_PASSWORD, REDIS_URI, REDIS_PORT, REDIS_DB)
