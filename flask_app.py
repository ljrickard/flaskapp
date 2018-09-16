#!/usr/bin/env python36
import os
import ast
import json
import config
import logging
import requests
import werkzeug
import time
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
from elasticsearch import Elasticsearch
from sites.brand_factory import Brands

app = Flask(__name__)
CORS(app)
config_object = 'config.{0}'.format(os.getenv('FLASK_CONFIGURATION', 'DevelopmentConfig'))
app.config.from_object(config_object)
logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s: (%(processName)s: %(process)d) %(levelname)-2s - %(module)-2s(%(lineno)d): %(message)s")
handler = TimedRotatingFileHandler('{0}/{1}-{2}.log'.format(app.config['LOG_DIR'], str(datetime.now()), os.getpid()), when='midnight', interval=1)
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
TASK_TYPES = ['search']

redis_connection = Redis._create_connection()
elasticsearch = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}])

logger.info('Config object loaded {0}'.format(config_object))

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/', methods=['GET'])
def default():
    return jsonify('hello')

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify('ok')

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/celery/conf', methods=['GET'])
def conf():
    return jsonify(celery.control.inspect().conf())

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/redis', methods=['GET'])
def redis_conn():
    return jsonify(str(redis_connection))

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/redis/keys', methods=['GET'])
def redis_keys():
    response = []
    for key in redis_connection.scan_iter("*"):
        response.append(str(key))
    return jsonify(response)

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/redis/ping', methods=['GET'])
def redis_ping():
    return jsonify(redis_connection.ping())

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/redis/flushall', methods=['POST'])
def redis_flushall():
    return jsonify(str(redis_connection.flushall()))

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/elasticsearch/info', methods=['GET'])
def elasticsearch_info():
    return jsonify(elasticsearch.info())

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/domain', defaults={'name': None}, methods=['GET'])
@app.route('/domain/<name>', methods=['GET'])
def domain(name):
    if name:
        total_products = elasticsearch.search(index="products", doc_type="skincare", body={"query": {"bool": {"filter": {"bool": {"must": [{"terms": {"brand": [name]}}]}}}}})['hits']['total']
        return jsonify({'total_products': total_products})

    domains = _get_domains()
    total_domains = len(domains)
    total_products = elasticsearch.search(index="products", body={"query": {"match_all": {}}})['hits']['total']
    return jsonify({'domains': domains, 'total_domains': total_domains, 'total_products': total_products})

def _get_domains():
    response = [domain for domain in redis_connection.lrange(DOMAINS, 0, -1)]
    if not response:
        raise InternalServerError("No domains found")
    else:
        return response

@app.errorhandler(werkzeug.exceptions.InternalServerError)
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
                raise BadRequest('{0} is not a valid domain'.format(domain))
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


def _get_task(task_id):
    task = redis_connection.hgetall(task_id)
    if not task:
        raise BadRequest()
    task['status'] = celery_task.AsyncResult(task_id).state
    return task


@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/task', methods=['POST'])
def task_post():
    _type = request.args.get('type')
    if not _type or _type not in TASK_TYPES:
        raise BadRequest('type is a required parameter')

    domain = request.args.get('domain')
    if not domain or domain not in _get_domains():
        raise BadRequest('domain is a required parameter')                             

    tasks = redis_connection.lrange(domain, 0, -1)
    for task_id in tasks:
        if celery_task.AsyncResult(task_id).state in ['PENDING', 'STARTED']:
            return jsonify(_get_task(task_id))
    
    task_id = str(celery_task.delay(domain, _type))
    task = {
                'id': task_id, 
                'type': _type,
                'domain': domain,
                'errors': None,
                'runtime': None,
                'result': None,
                'created_on': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
                '_links': { 'self': { 'href': '/task/{0}'.format(task_id) } }
            }

    redis_connection.lpush(domain, task_id)
    redis_connection.hmset(task_id, task)
    task['state'] = celery_task.AsyncResult(task_id).state
    response = {}
    response[domain] = task

    return jsonify(response)


@celery.task
def celery_task(domain, _type):
    logger.info('begin celery_task.....')
    start_time = time.time()
    id = celery_task.request.id

    try:
        task = redis_connection.hgetall(id)
        print(task)
        if _type == 'search':
            task['result'] = Brands(False).factory('kiehls').find_urls(redis_connection)

        task['runtime'] = calculate_run_time(start_time)
        redis_connection.hmset(id, task)

    except Exception as e:
        task = redis_connection.hgetall(id)
        errors = task['errors'].split()
        errors.append(str(e))
        task['errors'] = errors
        redis_connection.hmset(id, task)
        logger.error(str(e))
        
    logger.info('end celery_task.....')
    return id


def calculate_run_time(start_time):
    seconds = time.time() - start_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)



