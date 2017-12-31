#!/usr/bin/env python36
import os
import logging
import requests
import json
from celery import Celery
from flask import Flask, request, jsonify
from time import sleep
from werkzeug.exceptions import InternalServerError, BadRequest
from celery.task.control import inspect
from random import randint
import config
from app_redis import Redis


logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(
    'config.{0}'.format(os.getenv('FLASK_CONFIGURATION', 
                                        'DevelopmentConfig')))  

celery = Celery(
    app.name,
    backend=app.config['CELERY_RESULT_BACKEND'],
    broker=app.config['CELERY_BROKER_URL'])

celery.conf.update(app.config)

Redis.PORT = app.config['REDIS_PORT']
Redis.URI = app.config['REDIS_URI']
Redis.DB = app.config['REDIS_DB']

REDIS_KEY_SITES = 'sites'
FLOWERS_API = app.config['FLOWERS_API']

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    logger.info('healthcheck')
    return jsonify('ok')

# add celery as option 

@app.route('/celery', methods=['GET'])
def celery_ok():
    logger.info('celery check')
    if not inspect().stats():
        raise InternalServerError(description='celery not running')
    return jsonify('ok')


@app.route('/sites', methods=['GET', 'POST'])
def sites():
    redis_connection = Redis._create_connection()
    if request.method == 'POST':
        for site in request.data.decode('utf-8').split(','):
            redis_connection.lpush(REDIS_KEY_SITES, site)   
    return jsonify(redis_connection.lrange(REDIS_KEY_SITES, 0, -1))


@app.route('/scrape', methods=['POST'])
def scrape():
    async_results = []
    if request.data:
        for site in request.data.decode('utf-8').split(','):
            async_results.append(str(do_something_async.delay(60)))
    else:
        redis_connection = Redis._create_connection()
        all_sites = redis_connection.lrange(REDIS_KEY_SITES, 0, -1)
        for site in all_sites:
            async_results.append(str(do_something_async.delay(60)))   
    return jsonify(async_results)


@app.route('/tasks/status', methods=['GET'])
def tasks():
    return jsonify(str({key: {'state': value['state']} 
        for key, value in json.loads(
            requests.get('{0}{1}'.format(FLOWERS_API, '/tasks')).
                                                        text).items()}))


@app.route('/tasks/<uuid:id>/status', methods=['GET'])
def status(id):
    task = do_something_async.AsyncResult(str(id))
    return jsonify(
        {
            str(task.id): {
                'status':str(task.status), 
                'info':str(task.info)
            }
        })


@app.route('/tasks/<uuid:id>/result', methods=['GET'])
def result(id):
    logger.info('result')
    redis_connection = Redis._create_connection()
    result = redis_connection.get(id)
    if result:
        return jsonify(result)
    else:
        raise BadRequest(description='resource not found') 


@celery.task
def do_something_async(site):
    logger.info('starting to do something for {0}'.format(site))

    logger.info('{0}'.format(do_something_async.request))
    task_id = do_something_async.request.id
    logger.info('task id is:{0}'.format(task_id))
    random_int = randint(1, 100)
    logger.info('random_int is:{0}'.format(random_int))
    
    redis_connection = Redis._create_connection()
    redis_connection.set(str(task_id), random_int)
    
    logger.info('task_id type is:{0}'.format(type(task_id)))
    return task_id







