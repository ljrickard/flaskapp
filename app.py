#!/usr/bin/env python36
import os
import json
import config
import logging
import requests
from time import sleep
from celery import Celery
from random import randint
from datetime import datetime
from app_redis.app_redis import Redis
from celery.task.control import inspect
from flask import Flask, request, jsonify
from logging.handlers import TimedRotatingFileHandler
from werkzeug.exceptions import InternalServerError, BadRequest
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
config_object = 'config.{0}'.format(os.getenv('FLASK_CONFIGURATION', 'DevelopmentConfig'))
app.config.from_object(config_object)
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s")
handler = TimedRotatingFileHandler('{0}/{1}-{2}.log'.format(app.config['LOG_DIR'], str(datetime.now()), os.getpid()), when='H', interval=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)


celery = Celery(
    app.name,
    backend=app.config['CELERY_BROKER'],
    broker=app.config['CELERY_BROKER'],)

celery.conf.update(app.config)

Redis.PORT = app.config['REDIS_PORT']
Redis.URI = app.config['REDIS_URI']
Redis.DB = app.config['REDIS_DB']
Redis.PASSWORD = app.config['REDIS_PASSWORD']

REDIS_KEY_SITES = 'sites'
FLOWERS_API = app.config['FLOWERS_API']

logger.info('Config object loaded {0}'.format(config_object))

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify('ok')

@app.route('/conf', methods=['GET'])
def conf():
    return jsonify(celery.control.inspect().conf())

@app.route('/scheduled', methods=['GET'])
def scheduled():
    return jsonify(celery.control.inspect().scheduled())

@app.route('/active', methods=['GET'])
def active():
    return jsonify(celery.control.inspect().active())

@app.route('/reserved', methods=['GET'])
def reserved():
    return jsonify(celery.control.inspect().reserved())

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify(celery.control.inspect().stats())

@app.route('/registered_tasks', methods=['GET'])
def registered_tasks():
    return jsonify(celery.control.inspect().registered_tasks())

@app.route('/registered', methods=['GET'])
def registered():
    return jsonify(celery.control.inspect().registered())

@app.route('/sites', methods=['GET'])
def sites():
    redis_connection = Redis._create_connection()
    return jsonify(redis_connection.lrange(REDIS_KEY_SITES, 0, -1))

@app.route('/action', methods=['POST'])
def action():
    return jsonify(str(do_something_async.delay(60)))

@app.route('/tasks/status', methods=['GET'])
def tasks():
    return jsonify(str({key: {'state': value['state']} 
        for key, value in json.loads(
            requests.get('{0}{1}'.format(FLOWERS_API, '/tasks')).text).items()}))

@app.route('/tasks/<uuid:id>/status', methods=['GET'])
def status(id):
    try:
        return jsonify(do_something_async.AsyncResult(str(id)).status)
    except:
        raise BadRequest()

@app.route('/tasks/<uuid:id>/result', methods=['GET'])
def result(id):
    redis_connection = Redis._create_connection()
    result = redis_connection.get(id)
    if result:
        return jsonify(result)
    else:
        raise BadRequest() 

redis_connection = Redis._create_connection()

@app.route('/something', methods=['GET'])
def something():
    resturn jsonify([key in redis_connection.scan_iter("action:*")])

@celery.task
def do_something_async(site):
    logger.info('starting to do something.....')

    user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"} 

    # logger.info('{0}'.format(do_something_async.request))
    task_id = do_something_async.request.id
    logger.info('task id is:{0}'.format(task_id))
    
    #error handling not working! 

    key = 'action:{0}'.format(str(task_id))

    logger.info(key)

    try:
        response = redis_connection.hmset(key, user)   #set(str(task_id), random_int)
        logger.info("response")
        logger.info(response)

        response2 = redis_connection.hgetall(key)
        logger.info("response2")
        logger.info(response2)

    except e:
        logger.error(e)
    
    logger.info('finishing to do something.....')
    return task_id







