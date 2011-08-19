from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.conf import settings

class ContentTypeMapper(object):
    def __init__(self, item_type):
        self.item_type = item_type
        self.items = []
        self.discovered = False
    
    def autodiscover(self):
        if self.discovered:
            return
        if hasattr(settings, 'AMPCMS_APPLICATIONS'):
            for module in settings.AMPCMS_APPLICATIONS:
                #FIXME: change this to look for ampcms instead of content_manager and put it in a const file or something
                __import__(module, {}, {}, ['content_manager'])
        self.discovered = True
    
    def clear(self):
        self.items = None

    def register(self, name, item):
        assert issubclass(item, self.item_type)
        if name in dict(self.items).keys():
            raise ImproperlyConfigured('%s [%s] has already been registered' % (self.item_type, item))
        self.items.append((name, item))

    def get_items_dict(self):
        return dict(self.items)

    def get_item(self, name):
        item = self.get_items_dict().get(name)
        if item is None:
            raise ObjectDoesNotExist('%s [%s] has not been registered' % (self.item_type, name))
        else:
            return item