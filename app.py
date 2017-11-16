#!/usr/bin/env python36
import os
import logging
from celery import Celery
from flask import Flask
from time import sleep

logger = logging.getLogger(__name__)
app = Flask(__name__)

# with app.app_context():
#    app.config.from_object(
#        'config.{0}'.format(
#            os.getenv(
#                'FLASK_CONFIGURATION',
#                'DevelopmentConfig')))


# celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker = app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)


@app.route('/', methods=['POST'])
def hello_world():
    #result = do_something_async.delay(30)
    logger.info(str(result))
    return str(result)

#@celery.task


def do_something_async(t):
    logger.info('starting to do something for {0}'.format(t))
    sleep(t)
    logger.info('finished doing something for {0}'.format(t))


if __name__ == "__main__":
    app.run()
