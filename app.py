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

    for domain in domains:
        response[domain] = []
        for id in redis_connection.lrange(domain, 0, -1):
           response[domain].append(_get_task(id))

    return jsonify(response)


def _get_task(id):
    task = redis_connection.hgetall(id)
    func = Task.factory(task['type'])
    task['status'] = func.AsyncResult(id).state
    return task


class Task(object):
    def factory(type):
        if type == "search": 
            return search
        if type == "scrape": 
            return scrape
        else:
            raise BadRequest()


@app.route('/task', methods=['POST'])
def task_post():
    _type = request.args.get('type')
    domains = request.args.get('domain').split(',') if request.args.get('domain') else _get_domains()
    func = Task.factory(_type)
    try:
        kwargs = request.get_json(force=True)
    except:
        kwargs = {}
    
    response = {}
    for domain in domains:
        id = str(func.delay(domain, **kwargs))
        task = {
                    'id': id, 
                    'type': _type,
                    'domain': domain,
                    'kwargs': kwargs,
                    'error': None,
                    'created_on': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
                    '_links': { 'href': '/task/{0}'.format(id) }
                }

        redis_connection.lpush(domain, id)
        redis_connection.hmset(id, task)

        task['state'] = func.AsyncResult(id).state
        response[domain] = task

    return jsonify(response)


@app.route('/task/<id>', methods=['DELETE'])
def task_delete(id):
    task = _get_task(id)
    func = Task.factory(task['type'])

    if task['status'] in ['PENDING', 'STARTED']:
        revoke(id, terminate=True)
        while func.AsyncResult(id).state != 'REVOKED':
            sleep(0.1) 
        task['status'] = func.AsyncResult(id).state

    return jsonify(task)


@celery.task
def search(domain, **kwargs):
    logger.info('begin search.....')
    id = search.request.id
    random_number = randint(9, 19)

    try:
        logger.info('search sleeping for {0}'.format(random_number))
        sleep(random_number)

        task = redis_connection.hgetall(id)
        task['result'] = 'i did my task in only {0} seconds'.format(random_number)  # this is where the action will take place
        redis_connection.hmset(id, task)

    except Exception as e:
        task = redis_connection.hgetall(id)
        task['result'] = e
        redis_connection.hmset(id, task)
        logger.error(e)
        
    logger.info('end search.....')
    return id


@celery.task
def scrape(domain, **kwargs):
    logger.info('begin scrape_async.....')
    id = scrape_async.request.id
    key = 'scrape_async:{0}'.format(str(id))
    logger.info('task id for {0} and {1} is:{2}'.format(domain, site, id))
    random_number = randint(1, 9999)

    try:

        user = {
            'id': scrape_async.request.id, 
            'task': 'app.scrape_async', 
            'created_on': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
            'result': { random_number }, 
            'errors': {}
        } 

        response = redis_connection.hmset(key, user) 
        logger.info(response)

        response2 = redis_connection.hgetall(key)
        logger.info(response2)

    except Exception as e:
        logger.error(e)
        try:
            response = redis_connection.hmset(key, {'error': str(e)}) #this is a bit shit
            logger.info('Error logged to db={0}'.format(response))
        except Exception as e:
            logger.error(e)
        
    
    logger.info('end scrape_async.....')
    return id






