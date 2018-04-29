#!/usr/bin/env python36
import os
import ast
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
from celery.task.control import revoke
from domains.domain import Domain

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
app.logger.setLevel(logging.DEBUG)
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

DOMAINS = 'domains'
FLOWERS_API = app.config['FLOWERS_API']

redis_connection = Redis._create_connection()

logger.info('Config object loaded {0}'.format(config_object))

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify('ok')

@app.route('/celery/conf', methods=['GET'])
def conf():
    return jsonify(celery.control.inspect().conf())

@app.route('/redis/flushall', methods=['POST'])
def flushall():
    return jsonify(redis_connection.flushall())

@app.route('/domain', methods=['GET'])
def domain():
    return jsonify(_get_domains())

def _get_domains():
    return [domain for domain in redis_connection.lrange(DOMAINS, 0, -1)]

@app.route('/task', defaults={'id': None}, methods=['GET'])
@app.route('/task/<id>', methods=['GET'])
def task_get(id):
    if id and request.args.get('domain'):
        raise BadRequest()
    elif id:
        return jsonify(_get_task(id))
    elif request.args.get('domain'):
        domains = request.args.get('domain').split(',')
        for domain in domains:
            if domain not in _get_domains():
                raise BadRequest()
    else:
        domains = _get_domains()

    response = {}

    _type = request.args.get('type') if request.args.get('type') else None

    for domain in domains:
        response[domain] = []
        for id in redis_connection.lrange(domain, 0, -1):
            task = _get_task(id)
            if _type:
                if task['type'] == _type:
                    response[domain].append(task)
            else:
                response[domain].append(task)

    return jsonify(response)


def _get_task(id):
    task = redis_connection.hgetall(id)
    task['status'] = celery_task.AsyncResult(id).state
    return task


@app.route('/task', methods=['POST'])
def task_post():
    _type = request.args.get('type')
    domains = request.args.get('domain').split(',') if request.args.get('domain') else _get_domains()

    try:
        kwargs = request.get_json(force=True)
    except:
        kwargs = {}
    
    response = {}
    for domain in domains:
        id = str(celery_task.delay(domain, **kwargs))
        task = {
                    'id': id, 
                    'type': _type,
                    'domain': domain,
                    'kwargs': kwargs,
                    'errors': '',
                    'created_on': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
                    '_links': { 'href': '/task/{0}'.format(id) }
                }

        redis_connection.lpush(domain, id)
        redis_connection.hmset(id, task)

        task['state'] = celery_task.AsyncResult(id).state
        response[domain] = task

    return jsonify(response)


@app.route('/task/<id>', methods=['DELETE'])
def task_delete(id):
    task = _get_task(id)

    if task['status'] in ['PENDING', 'STARTED']:
        revoke(id, terminate=True)
        while celery_task.AsyncResult(id).state != 'REVOKED':
            sleep(0.1) 
        task['status'] = celery_task.AsyncResult(id).state

    return jsonify(task)


@celery.task
def celery_task(domain, **kwargs):
    logger.info('begin celery_task.....')
    id = celery_task.request.id
    random_number = randint(9, 19)

    try:
        logger.info('celery_task sleeping for {0}'.format(random_number))
        sleep(random_number)

        task = redis_connection.hgetall(id)
        
        Domain().factory(domain).search()

        task['result'] = 'i did my task in only {0} seconds'.format(random_number)  # this is where the action will take place
        redis_connection.hmset(id, task)

    except Exception as e:
        task = redis_connection.hgetall(id)
        errors = task['errors'].split()
        errors.append(e)
        task['errors'] = errors
        redis_connection.hmset(id, task)
        logger.error(e)
        
    logger.info('end celery_task.....')
    return id





