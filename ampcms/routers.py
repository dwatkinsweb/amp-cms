from ampcms.utils import get_current_request
from ampcms.conf import settings

class HostBasedRouter(object):
    def db_for_read(self, model, **hints):
        from ampcms.models import Site
        request = get_current_request()
        if request is not None:
            site = Site.objects.using(settings.AMPCMS_ROOT_DATABASE).get_current_by_request(request)
            if site.database_name is not None and site.database_name in settings.DATABASES:
                return site.database_name
            elif site.name is not None and site.name in settings.DATABASES:
                return site.name
    db_for_write = db_for_read