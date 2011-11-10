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

from ampcms.lib import layouts, pages
from ampcms.decorators import acl_required
from ampcms import const as C
from django.core.urlresolvers import resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django_genshi import RequestContext, render_to_response #@UnresolvedImport
from genshi.core import Markup #@UnresolvedImport

import logging
log = logging.getLogger(__name__)

def login(request, *args, **kwargs):
    view, args, kwargs = resolve(settings.AMPCMS_LOGIN_URL, settings.AMPCMS_LOGIN_URLCONF)
    if request.GET.has_key('next'):
        kwargs.update({'callback_url': request.GET['next']})
    else:
        kwargs.update({'callback_url': '/'})
    response = view(request, *args, **kwargs)
    if isinstance(response, HttpResponseRedirect):
        return response
    
    context = RequestContext(request)
    context.update({'content': Markup(response.content)})
    response = render_to_response('ampcms/login.html', context)
    return response

def logout(request, *args, **kwargs):
    view, args, kwargs = resolve(settings.AMPCMS_LOGOUT_URL, settings.AMPCMS_LOGOUT_URLCONF)
    kwargs.update({'callback_url': '/login'})
    return view(request, *args, **kwargs)

@acl_required()
def index(request, *args, **kwargs):
    log.debug('ampcms.views.index - start')
    page = kwargs.pop(C.EXTRA_KWARGS_PAGE)
    page_content = pages.page_mapper.get_item(page.page_class)(request=request, request_kwargs=kwargs, page=page)
    layout = layouts.PCLayout(request=request, request_kwargs=kwargs, page=page_content)
    log.debug('ampcms.views.index - end')
    return HttpResponse(layout.html())

@acl_required()
def full_page(request, *args, **kwargs):
    log.debug('ampcms.views.full_page - start')
    page = kwargs.pop(C.EXTRA_KWARGS_PAGE)
    log.debug('page: %s' % (page))
    page_content = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    layout = layouts.PCLayout(user=request.user, page=page_content, request=request, request_kwargs=kwargs)
    log.debug('ampcms.views.full_page - end')
    return HttpResponse(layout.html())
    
@acl_required()
def page(request, *args, **kwargs):
    log.debug('ampcms.views.page - start')
    page = kwargs.pop(C.EXTRA_KWARGS_PAGE)
    log.debug('page: %s' % (page))
    page_content = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    log.debug('ampcms.views.page - end')
    return HttpResponse(page_content.html())

@acl_required()
def pagelet(request, *args, **kwargs):
    log.debug('ampcms.views.pagelet - start')
    page= kwargs.pop(C.EXTRA_KWARGS_PAGE)
    log.debug('page: %s' % (page))
    page_content = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    pagelet_name = kwargs.get(C.URL_KEY_PAGELET)
    pagelet_url = kwargs.get(C.URL_KEY_PAGELET_URL)
    log.debug('pagelet: %s - %s' % (pagelet_name, pagelet_url))
    pagelet_content = page_content.get_pagelet(pagelet_name)
    log.debug('ampcms.views.pagelet - end')
    if pagelet_url:
        process_url = '/'+pagelet_url
    else:
        process_url = '/'
    pagelet_json = pagelet_content.json(process_url)
    if isinstance(pagelet_json, HttpResponse):
        response = pagelet_json
    else: 
        response = HttpResponse(pagelet_json)
    # TODO: Come up with a better way to ignore cache for IE
    if 'MSIE' in request.META['HTTP_USER_AGENT']:
        response['Cache-Control'] = 'max-age=0,no-cache,no-store,post-check=0,pre-check=0'
    return response

@acl_required()
def css(request, *args, **kwargs):
    # TODO: remove acl_required decorator. Currently needed to be able to load the models correctly.
    ''' Build the css for the page based on page and pagelets '''
    log.debug('ampcms.views.css - start')
    page = kwargs.pop(C.EXTRA_KWARGS_PAGE)
    page_content = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    layout = layouts.PCLayout(user=request.user, page=page_content, request=request, request_kwargs=kwargs)
    log.debug('ampcms.views.css - end')
    return HttpResponse(layout.css(), mimetype='text/css')
