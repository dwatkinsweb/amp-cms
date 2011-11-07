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

from django.conf import settings as django_settings

settings = django_settings

settings.AMPCMS_CACHING = getattr(django_settings, 'AMPCMS_CACHING', False)
settings.AMPCMS_CACHING_TIMEOUT = getattr(settings, 'AMPCMS_CACHING_TIMEOUT', 0)
settings.AMPCMS_AUTH_PROFILE_MODEL = getattr(django_settings, 'AMPCMS_AUTH_PROFILE_MODEL', None)
settings.AMPCMS_MEDIA_URL = getattr(django_settings, 'AMPCMS_MEDIA_URL', '%sampcms/' % django_settings.MEDIA_URL)
settings.AMPCMS_APPLICATIONS = getattr(django_settings, 'AMPCMS_APPLICATIONS', [])
settings.AMPCMS_ADD_APPLICATION_URLS = getattr(django_settings, 'AMPCMS_ADD_APPLICATION_URLS', False)
settings.AMPCMS_LOGIN_URL = getattr(django_settings, 'AMPCMS_LOGIN_URL', '/login')
settings.AMPCMS_LOGIN_URLCONF = getattr(django_settings, 'AMPCMS_LOGIN_URLCONF', 'auth.urls')
settings.AMPCMS_LOGOUT_URL = getattr(django_settings, 'AMPCMS_LOGOUT_URL', '/logout')
settings.AMPCMS_LOGOUT_URLCONF = getattr(django_settings, 'AMPCMS_LOGOUT_URLCONF', 'auth.urls')
settings.AMPCMS_PAGELET_LAYOUTS = getattr(django_settings, 'AMPCMS_PAGELET_LAYOUTS', [])
settings.AMPCMS_PUBLIC_URL = getattr(django_settings, 'AMPCMS_PUBLIC_URL', '/')
settings.AMPCMS_PERMISSION_DENIED_URL = getattr(django_settings, 'AMPCMS_PERMISSION_DENIED_URL', '/')
settings.AMPCMS_WYSIWYG = getattr(django_settings, 'AMPCMS_WYSIWYG', False)
settings.AMPCMS_ROOT_DATABASE = getattr(django_settings, 'AMPCMS_ROOT_DATABASE', 'ampcms')
