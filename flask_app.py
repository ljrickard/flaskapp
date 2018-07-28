#!/usr/bin/env python36
import os
import ast
import json
import config
import logging
import requests
import werkzeug
from time import sleep
from celery import Celery
from random import randint
from datetime import datetime
from app_redis.app_redis import Redis
from celery.task.control import inspect
from flask import Flask, request, jsonify
from logging.handlers import TimedRotatingFileHandler
from werkzeug.exceptions import InternalServerError, BadRequest
# from flask_cors import CORS
from celery.task.control import revoke
from domains.domain import Domain
from elasticsearch import Elasticsearch

app = Flask(__name__)
# CORS(app)
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
        raise InternalServerError()
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


@app.errorhandler(werkzeug.exceptions.InternalServerError)
@app.route('/task', methods=['POST'])
def task_post():
    _type = request.args.get('type')
    all_domains = _get_domains()
    if request.args.get('domain'):
        domains = request.args.get('domain').split(',')
        for domain in domains:
            if domain not in all_domains:
                raise BadRequest()
    else:
        domains = all_domains

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
                    '_links': { 'self': { 'href': '/task/{0}'.format(id) } }
                }

        redis_connection.lpush(domain, id)
        redis_connection.hmset(id, task)

        task['state'] = celery_task.AsyncResult(id).state
        response[domain] = task

    return jsonify(response)


@app.errorhandler(werkzeug.exceptions.InternalServerError)
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





