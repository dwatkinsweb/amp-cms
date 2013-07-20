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

# STATIC_URL
settings.AMPCMS_STATIC_URL = getattr(settings, 'AMPCMS_STATIC_URL', getattr(settings, 'AMPCMS_MEDIA_URL', '%sampcms/' % settings.STATIC_URL))
# List of django applications to use in ampcms
settings.AMPCMS_APPLICATIONS = getattr(settings, 'AMPCMS_APPLICATIONS', [])
# Public url to redirect to when a unauthorized user accesses site
settings.AMPCMS_PUBLIC_URL = getattr(settings, 'AMPCMS_PUBLIC_URL', '/')
# Permission denied url when user accesses page/pagelet they don't have permissions for
settings.AMPCMS_PERMISSION_DENIED_URL = getattr(settings, 'AMPCMS_PERMISSION_DENIED_URL', '/')
# Path to the javascript config file
settings.AMPCMS_JAVASCRIPT_CONFIG = getattr(settings, 'AMPCMS_JAVASCRIPT_CONFIG', None)
# Folder to look in for skins
settings.AMPCMS_SKIN_FOLDER = getattr(settings, 'AMPCMS_SKIN_FOLDER', 'ampcms_skins')
# Flag to display attempt to display a fully function debug exception page for uncaught exceptions while in debug mode
settings.AMPCMS_USE_AMPCMS_DEBUG = getattr(settings, 'AMPCMS_USE_AMPCMS_DEBUG', False)
# Title for 404 page/pagelet
settings.AMPCMS_404_TITLE = getattr(settings, 'AMPCMS_404_TITLE', 'Page Not Found')
# Title for 403 page/pagelet
settings.AMPCMS_403_TITLE = getattr(settings, 'AMPCMS_403_TITLE', 'Permission Denied')
# Title for 500 page/pagelet
settings.AMPCMS_500_TITLE = getattr(settings, 'AMPCMS_500_TITLE', 'Error Processing Request')
# Layouts to assign to pages - This just gives an extra class to the page element
settings.AMPCMS_PAGELET_LAYOUTS = getattr(settings, 'AMPCMS_PAGELET_LAYOUTS', [])
# wysiwyg to use for admin
settings.AMPCMS_WYSIWYG = getattr(settings, 'AMPCMS_WYSIWYG', False)
# Template handling
settings.AMPCMS_BASE_TEMPLATE = getattr(settings, 'AMPCMS_BASE_TEMPLATE', 'base.html')
settings.AMPCMS_RESPONSE_CLASS = getattr(settings, 'AMPCMS_RESPONSE_CLASS', None)
# Turn django-cache-machine on/off and set timeout
settings.AMPCMS_CACHING = getattr(settings, 'AMPCMS_CACHING', False)
settings.AMPCMS_CACHING_TIMEOUT = getattr(settings, 'AMPCMS_CACHING_TIMEOUT', 0)

# TODO: Remove the need for any of this
settings.AMPCMS_ACCOUNT_URLCONF = getattr(settings, 'AMPCMS_ACCOUNT_URLCONF', 'auth.urls')
settings.AMPCMS_ACCOUNT_LOGIN_URL = getattr(settings, 'AMPCMS_ACCOUNT_LOGIN_URL', '/login')
settings.AMPCMS_ACCOUNT_REGISTER_URL = getattr(settings, 'AMPCMS_ACCOUNT_REGISTER_URL', '/register')
settings.AMPCMS_ACCOUNT_FORGOT_PASSWORD_URL = getattr(settings, 'AMPCMS_ACCOUNT_FORGOT_PASSWORD_URL', '/forgot_password')
settings.AMPCMS_ACCOUNT_UPDATE_PASSWORD_URL = getattr(settings, 'AMPCMS_ACCOUNT_UPDATE_PASSWORD_URL', '/update_password')
settings.AMPCMS_ACCOUNT_ALLOW_REGISTRATION = getattr(settings, 'AMPCMS_ACCOUNT_ALLOW_REGISTRATION', False)
settings.AMPCMS_ACCOUNT_LOGOUT_URL = getattr(settings, 'AMPCMS_ACCOUNT_LOGOUT_URL', '/logout')
settings.AMPCMS_ACCOUNT_NO_PERMISSIONS_URL = getattr(settings, 'AMPCMS_ACCOUNT_NO_PERMISSIONS_URL', '/no_permissions')