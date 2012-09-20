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

from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django_genshi.shortcuts import render_to_response as django_render_to_response

import os

class AMPCMSAjaxResponse(object):
    def __init__(self, response):
        self.response = response
    @property
    def cookies(self):
        if hasattr(self.response, 'cookies'):
            return self.response.cookies
        else:
            return []

class HttpResponseSSLRedirect(object):
    cookies = []

class AMPCMSMedia(object):
    def __init__(self, site, title, css, js):
        self.title = title
        self.site = site
        self._css = css
        self.js = js
    
    @property
    def css(self):
        css_files = []
        for css in self._css:
            if 'HTTP://' in css or settings.MEDIA_URL in css:
                pass
            elif self.site.skin is not None and os.path.exists('%scss/%s/%s' % (settings.MEDIA_ROOT, self.site.skin, css)):
                css = '%scss/%s/%s' % (settings.MEDIA_URL, self.site.skin, css)
            else:
                css = '%scss/%s' % (settings.MEDIA_URL, css)
            css_files.append(css)
        return css_files

class HttpResponseFullRedirect(HttpResponseRedirect):
    pass

class HttpFixedResponse(HttpResponse):
    pass

def render_to_response(template_name, dictionary=None, context_instance=None):
    if dictionary is not None:
        request = dictionary.get('request')
        if request is not None:
            from ampcms.models import AmpCmsSite
            site = AmpCmsSite.objects.get_by_request(request)
            if site.skin is not None:
                skin_template = '%s/%s' % (site.skin, template_name)
                if not isinstance(template_name, list):
                    template_name = [template_name]
                template_name.insert(0, skin_template)
    return django_render_to_response(template_name, dictionary, context_instance)
    