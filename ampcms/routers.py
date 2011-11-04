from ampcms.utils import get_current_request
from django.conf import settings

class HostBasedRouter(object):
    def db_for_read(self, model, **hints):
        request = get_current_request()
        if request is not None:
            host = request.get_host()
            if host in settings.DATABASES:
                return host
    db_for_write = db_for_read