import redis
import logging
from werkzeug.exceptions import InternalServerError

logger = logging.getLogger(__name__)

class Redis:
	URI=None
	PORT=None
	DB=None
	PASSWORD=None

	@classmethod
	def _create_connection(cls):
		try:
			redis_connection = redis.StrictRedis(host=cls.URI, port=cls.PORT, db=cls.DB, password=cls.PASSWORD, charset="utf-8", decode_responses=True)
			logger.info(redis_connection)
		except redis.ConnectionError:
			raise InternalServerError(description='redis ConnectionError')
		return redis_connection