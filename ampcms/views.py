from ampcms.lib import layouts, pages
from ampcms.decorators import acl_required
from ampcms.conf import settings
from django.core.urlresolvers import resolve
from django.http import HttpResponse, HttpResponseRedirect
from django_genshi import RequestContext, render_to_response
from genshi.core import Markup

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
    page = kwargs.pop('page_model')
    page_object = pages.page_mapper.get_item(page.page_class)(request=request, request_kwargs=kwargs, page=page)
    # TODO(cm): need to get the layout based on meta[user_agent]
    layout = layouts.PCLayout(request=request, request_kwargs=kwargs, page=page_object)
    log.debug('ampcms.views.index - end')
    return HttpResponse(layout.html())

@acl_required()
def full_page(request, *args, **kwargs):
    log.debug('ampcms.views.full_page - start')
    page = kwargs.pop('page_model')
    page_object = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    # TODO(cm): need to get the layout based on meta[user_agent]
    layout = layouts.PCLayout(user=request.user, page=page_object, request=request, request_kwargs=kwargs, block_load=True)
    log.debug('ampcms.views.full_page - end')
    return HttpResponse(layout.html())
    
@acl_required()
def page(request, *args, **kwargs):
    log.debug('ampcms.views.page - start')
    page = kwargs.pop('page_model')
    page_object = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    log.debug('ampcms.views.page - end')
    return HttpResponse(page_object.html())

@acl_required()
def pagelet(request, *args, **kwargs):
    log.debug('ampcms.views.pagelet (%s, %s) - start' % (kwargs.get('pagelet', ''), kwargs.get('url', '')))
    page = kwargs.pop('page_model')
    page_object = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    pagelet_object = page_object.get_pagelet(kwargs.get('pagelet'))
    log.debug('ampcms.views.pagelet - end')
    if kwargs.get('url'):
        process_url = '/'+kwargs['url']
    else:
        process_url = '/'
    return HttpResponse(pagelet_object.json(process_url))

@acl_required()
def css(request, *args, **kwargs):
    # TODO(cm): This probably shouldn't use acl_required
    ''' Build the css for the page based on page and pagelets '''
    log.debug('ampcms.views.css - start')
    page = kwargs.pop('page_model')
    page_object = pages.page_mapper.get_item(page.page_class)(page=page, request=request, request_kwargs=kwargs)
    layout = layouts.PCLayout(user=request.user, page=page_object, request=request, request_kwargs=kwargs, block_load=True)
    log.debug('ampcms.views.css - end')
    return HttpResponse(layout.css(), mimetype='text/css')