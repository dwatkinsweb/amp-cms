#-------------------------------------------------------------------------------
# Copyright David Watkins 2011
# 
# AMP-CMS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from ampcms.conf import settings
from ampcms import const as C

class ContentTypeMapper(object):
    def __init__(self, item_type):
        self.item_type = item_type
        self.items = []
        self.discovered = False
    
    def autodiscover(self):
        if self.discovered:
            return
        if settings.AMPCMS_APPLICATIONS:
            for module in settings.AMPCMS_APPLICATIONS:
                __import__(module, {}, {}, [C.APPLICATION_INITIALIZATION_MODULE])
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
