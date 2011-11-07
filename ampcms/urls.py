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
application_mapper.autodiscover()

urlpatterns = patterns('ampcms.views',
    url(r'^login/?$',
        view='login', name='login'),
    url(r'^logout/?$',
        view='logout', name='logout'),
    url(r'^page/(?P<module>[a-zA-Z0-9]+)/(?P<page>[a-zA-Z0-9]+)/?$', 
        view='page', name='page'),
    url(r'^pagelet/(?P<module>[a-zA-Z0-9_]+)/(?P<page>[a-zA-Z0-9_]+)/(?P<pagelet>[a-zA-Z0-9_]+)/?(?P<url>[a-zA-Z0-9\/\-_]+)?', 
        view='pagelet', name='pagelet'),
    url(r'^css/(?P<module>[a-zA-Z0-9_]+)/(?P<page>[a-zA-Z0-9_]+)/?$', 
        view='css', name='css'),
    url(r'^(?P<module>[a-zA-Z0-9_]+)/?(?P<page>[a-zA-Z0-9_]+)?/?$', 
        view='full_page', name='full_page'),
    url(r'^$', 
        view='index', name='index')
)
