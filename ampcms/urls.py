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

from django.conf.urls.defaults import patterns, url

from ampcms.lib.application_mapper import application_mapper
from ampcms.conf import settings
from ampcms import const as C

application_mapper.autodiscover()

urlpatterns = patterns('ampcms.views',
    url(r'^login/?$',
        view='account_handling',
        name='login',
        kwargs={'url':settings.AMPCMS_ACCOUNT_LOGIN_URL,
                'title': 'Login'}),
    url(r'^register/?$',
        view='account_handling',
        name='register',
        kwargs={'url':settings.AMPCMS_ACCOUNT_REGISTER_URL,
                'title': 'Registration',
                'allow_registration':settings.AMPCMS_ACCOUNT_ALLOW_REGISTRATION}),
    url(r'^forgot_password/?$',
        view='account_handling',
        name='forgot_password',
        kwargs={'url':settings.AMPCMS_ACCOUNT_FORGOT_PASSWORD_URL,
                'title': 'Forgot Password'}),
    url(r'^update_password/?$',
        view='account_handling',
        name='update_password',
        kwargs={'url':settings.AMPCMS_ACCOUNT_UPDATE_PASSWORD_URL,
                'title': 'Update Password'}),
    url(r'^no_permissions/?$',
        view='account_handling',
        name='no_permissions',
        kwargs={'url':settings.AMPCMS_ACCOUNT_NO_PERMISSIONS_URL,
                'title': 'No Permissions'}),
    url(r'^logout/?$',
        view='logout',
        name='logout'),
    url(r'^page/(?P<%s>[a-zA-Z0-9]+)/(?P<%s>[a-zA-Z0-9]+)/?$'
            % (C.URL_KEY_MODULE, C.URL_KEY_PAGE),
        view=C.VIEW_NAME_PAGE,
        name=C.VIEW_NAME_PAGE),
    url(r'^pagelet/(?P<%s>[a-zA-Z0-9_]+)/(?P<%s>[a-zA-Z0-9_]+)/(?P<%s>[a-zA-Z0-9_]+)/?(?P<%s>[a-zA-Z0-9\/\-_]+)?'
            % (C.URL_KEY_MODULE, C.URL_KEY_PAGE, C.URL_KEY_PAGELET, C.URL_KEY_PAGELET_URL),
        view=C.VIEW_NAME_PAGELET,
        name=C.VIEW_NAME_PAGELET),
    url(r'^css/(?P<%s>[a-zA-Z0-9_]+)/(?P<%s>[a-zA-Z0-9_]+)/?$'
            % (C.URL_KEY_MODULE, C.URL_KEY_PAGE),
        view=C.VIEW_NAME_CSS,
        name=C.VIEW_NAME_CSS),
    url(r'^(?P<%s>[a-zA-Z0-9_]+)/?(?P<%s>[a-zA-Z0-9_]+)?/?$'
            % (C.URL_KEY_MODULE, C.URL_KEY_PAGE),
        view=C.VIEW_NAME_FULL_PAGE,
        name=C.VIEW_NAME_FULL_PAGE),
    url(r'^$', 
        view=C.VIEW_NAME_INDEX,
        name=C.VIEW_NAME_INDEX)
)
