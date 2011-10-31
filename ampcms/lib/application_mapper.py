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

from content_type_mapper import ContentTypeMapper
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class AmpCmsApplication(object):
    def __init__(self, urlconf=settings.ROOT_URLCONF, url_prefix=None):
        self.urlconf = urlconf
        self.url_prefix = url_prefix

class ApplicationMapper(ContentTypeMapper):
    def register(self, name, item):
        assert isinstance(item, self.item_type)
        if name in dict(self.items).keys():
            raise ImproperlyConfigured('%s [%s] has already been registered' % (self.item_type, item))
        self.items.append((name, item))

application_mapper = ApplicationMapper(AmpCmsApplication)
