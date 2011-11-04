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

from django.conf import settings

import os

class AMPCMSAjaxResponse(object):
    def __init__(self, response):
        self.response = response

class AMPCMSMedia(object):
    def __init__(self, site, css, js):
        self.site = site
        self._css = css
        self.js = js
    
    @property
    def _get_css(self):
        css_files = []
        for css in self._css:
            if settings.MEDIA_URL in css:
                css_files.append(css)
            elif self.site.skin is not None and os.path.exists('%s/css/%s/%s' % (settings.MEDIA_ROOT, self.site.skin, css)):
                css_files.append('%s/css/%s/%s' % (settings.MEDIA_URL, self.site.skin, css))
            else:
                css_files.append('%s/css/%s' % (settings.MEDIA_URL, css))
        return css_files
