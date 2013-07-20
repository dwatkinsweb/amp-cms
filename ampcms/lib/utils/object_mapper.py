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

class BaseObjectMapper(object):
    object_types = ()
    item_type = 'object'
    
    def __init__(self):
        self.clear()

    def clear(self):
        self.data = {}
        self.discovered = False
    
    def autodiscover(self):
        if self.discovered:
            return
        if settings.AMPCMS_APPLICATIONS:
            for module in settings.AMPCMS_APPLICATIONS:
                __import__(module, {}, {}, [C.APPLICATION_INITIALIZATION_MODULE])
        self.discovered = True

    def register(self, name, item):
        self.item_assertion(item)
        if name in self.data:
            raise ImproperlyConfigured('%s [%s] has already been registered' % (self.item_type, item))
        self.data[name] = item

    def item_assertion(self, item):
        assert issubclass(item, self._get_object_types())

    def get_item(self, name):
        item = self.data.get(name)
        if item is None:
            raise ObjectDoesNotExist('%s [%s] has not been registered' % (self.item_type, name))
        else:
            return item
    
    def items(self):
        return [(k, self.data[k]) for k in sorted(self.data)]
    
    def _get_object_types(self):
        if self.object_types is None:
            raise ImproperlyConfigured('%s has no object_types defined')
        else:
            return self.object_types