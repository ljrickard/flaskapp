import logging
import uuid
from datetime import datetime
from data_access.data_access import DataAccess

logger = logging.getLogger(__name__)


class Website(object):

    def __init__(self, dry_run):
        self.data_access = DataAccess(dry_run)
        self.product_template = self.data_access.get_product_template()

    def find_urls(self, redis_connection):
        response = []
        urls = self.get_urls()
        for url in urls:
            if not redis_connection.get(url):
                id = str(uuid.uuid4())
                details = {
                    'id': id,
                    'domain': self.brand,
                    'url': url,
                    'created_on': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_on': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    'prod_on': None,
                    'data': None, 
                    '_links': { 'self': 
                        { 
                            'href': '/id/{0}'.format(id)
                        },
                        'scrape': 
                        { 
                            'href': '/id/{0}/{1}'.format(id, '?type=scrape')
                        }  
                    },
                    'is_valid': self.is_valid(url),
                    'in_prod': False
                }
                response.append(details)
                redis_connection.set(url, id)
                redis_connection.hmset(id, details)
            
        return response
        # add if already exits
        # return self.data_access.filter_existing_products(self.brand, product_urls)


    def scrape_url(self, url):
        return self.scrape_product_url([url])

