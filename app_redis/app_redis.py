import redis
from werkzeug.exceptions import InternalServerError

class Redis:
	URI = None
	PORT = None
	DB = None

	@classmethod
	def _create_connection(cls):
	    try:
	        redis_connection = redis.StrictRedis(host=cls.URI, port=cls.PORT, db=cls.DB)
	    except redis.ConnectionError:
	        raise InternalServerError(description='redis ConnectionError')
	    return redis_connection