from content_type_mapper import ContentTypeMapper
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class AmpCmsApplication(object):
    def __init__(self, urls=settings.ROOT_URLCONF):
        self.urlconf = urls

class ApplicationMapper(ContentTypeMapper):
    def register(self, name, item):
        assert isinstance(item, self.item_type)
        if name in dict(self.items).keys():
            raise ImproperlyConfigured('%s [%s] has already been registered' % (self.item_type, item))
        self.items.append((name, item))

application_mapper = ApplicationMapper(AmpCmsApplication)