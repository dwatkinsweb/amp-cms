from ampcms.lib.http.request import get_current_request
from ampcms.conf import settings
import lib

class HostBasedRouter(object):
    def db_for_read(self, model, **hints):
        request = get_current_request()
        if request is not None:
            host = request.get_host()
            database = lib.get_database_by_host(host)
            if database is not None:
                return database
            elif host in settings.DATABASES:
                return host
    db_for_write = db_for_read