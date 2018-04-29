from domains.kiehls import Kiehls
from werkzeug.exceptions import BadRequest

class Domain(object):

    def factory(self, domain):
        if domain == "kiehls":
            return Kiehls()
        else:
        	raise BadRequest()

