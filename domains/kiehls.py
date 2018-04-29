import logging
from domains.website import Website

logger = logging.getLogger(__name__)

BRAND = "Kiehls"
BASE_URL = "http://www.kiehls.co.uk"
SITE_MAP = "/site-map.html"
SITE_MAP_KEYWORD = 'skin-care'  # create regex containing skin care + base url

class Kiehls(Website):

	def __init__(self):
	    super(Kiehls, self).__init__()
	    self.base_url = BASE_URL
	    self.brand = BRAND

	def search(self):
		return super(Kiehls, self).search()

	def scrape(self):
		return super(Kiehls, self).scrape()

	def promote(self):
		return super(Kiehls, self).promote()

