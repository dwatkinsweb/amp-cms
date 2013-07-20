from ampcms.lib.http.request import get_current_request
from ampcms.conf import settings

class HostBasedRouter(object):
    def db_for_read(self, model, **hints):
        request = get_current_request()
        if request is not None:
            host = request.get_host()
            database_names = settings.AMPCMS_HOST_DATABASES[host]
            if database_names is not None and database_names in settings.DATABASES:
                return database_names
            elif host is not None and host in settings.DATABASES:
                return host
    db_for_write = db_for_read