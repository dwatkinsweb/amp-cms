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

from genshi.core import Markup #@UnresolvedImport
from django_genshi.shortcuts import render_to_stream #@UnresolvedImport
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import resolve, set_urlconf, get_resolver
from django.contrib import messages

from ampcms.lib.content_type import BaseContentType
from ampcms.lib.content_type_mapper import ContentTypeMapper
from ampcms.lib.application_mapper import application_mapper
from ampcms.lib.response import AMPCMSAjaxResponse, HttpFixedResponse, HttpResponseFullRedirect, HttpResponseSSLRedirect
from ampcms import const as C

from ampcms.conf import settings

import json
import urllib
import os

import logging
log = logging.getLogger(__name__)

class BasePagelet(BaseContentType):
    '''
    Base pagelet object for all pagelets to extend.
    This contains the base functionality for generating content, css, and js for the pagelets.
    Only methods that should need to be overwritten are _get_context and _get_template.
    Will look in /pagelets folder when grabbing media and templates
    '''
    def __init__(self, pagelet=None, template='pagelets/base.html', **kwargs):
        '''
        @param pagelet: pagelet instance from the pagelet model
        @param template: name of the template
        @param classes: any other css classes to add to pagelet
        '''
        super(BasePagelet, self).__init__(**kwargs)
        self._data_model = pagelet
        self._template = template
        self.view_css = []
        self.view_js = []
    
    def _get_html_data(self):
        if self._data_model is not None:
            data = {C.HTML_DATA_TAG_KEY_NAME : self._data_model.name}
        else:
            data = {}
        return data
    
    def _build_css(self):
        '''
        Build the css based on any pagelet attributes
        '''
        css = self.view_css
        if css is not None and not isinstance(css, list):
            css = [val.strip() for val in css.split(',')]
        return filter(None, css)
    
    def _build_js(self):
        '''
        Build the js based on any pagelet attributes
        '''
        js = self.view_js
        if js is not None and not isinstance(js, list):
            js = [val.strip() for val in js.split(',')]
        return filter(None, js)

class MenuPagelet(BasePagelet):
    '''
    Pagelet used to build a menu. This is not a pagelet that 
    '''
    def __init__(self, label=None, selected_item=None, template='pagelets/menu.html', **kwargs):
        '''
        Initialize the menu. Default this pagelet to None because the pagelet may not be created from the database.
        @param menu_label: label of the menu used as the <ul> class and id
        @param selected_item: selected menu item will be flagged with a class of selected
        @param template: list of menu children. Each item needs to be in a tuple(label, href) format
        '''
        super(MenuPagelet, self).__init__(**kwargs)
        self.label = label
        self.selected_item = selected_item
        self._template = template
        self._children = []
    
    def append(self, label, href, icon=None):
        '''
        Manually append a new item to the menu
        @param label: label to be display for the menu
        @param href: url for the menu item
        '''
        self._children.append((label,href, icon))
    
    def _get_context(self):
        context = super(MenuPagelet, self)._get_context()
        context.update({C.CONTENT_TYPE_CONTEXT_MENU_LABEL: self.label,
                        C.CONTENT_TYPE_CONTEXT_SELECTED_ITEM : self.selected_item})
        return context
    
    def _get_html_data(self):
        data = {C.HTML_DATA_TAG_KEY_NAME : self.label}
        return data
    
    def _build_css(self):
        '''
        Return the css based on the menu_label
        '''
        _css = '%s.css' % self.label
        self._css = [_css]
        site = self.request_kwargs['site_model']
        if site.skin is not None and os.path.exists('%scss/%s/%s' % (settings.MEDIA_ROOT, site.skin, _css)):
            self._css.append('%scss/%s/%s' % (settings.MEDIA_URL, site.skin, _css))
        return self._css

class SimplePagelet(BasePagelet):
    '''
    Simple container that displays a small bit of html output
    '''
    def __init__(self, template='pagelets/simple.html', **kwargs):
        super(SimplePagelet, self).__init__(**kwargs)
        self._template = template
    
    def _get_context(self):
        context = super(SimplePagelet, self)._get_context()
        context['content'] = Markup(self._data_model.content or '')
        return context

class ApplicationPagelet(BasePagelet):
    '''
    A pagelet that creates its content based on the url of another application. 
    It will display the application within the pagelet.
    '''
    def __init__(self, template='pagelets/application.html', **kwargs):
        super(ApplicationPagelet, self).__init__(**kwargs)
        self._template = template
        self.process_url = None
        self.title = self._data_model.title
        
    def html(self, include_content=None):
        return self._to_stream(include_content).render()

    def _to_stream(self, include_content=None):
        '''
        Renders the pagelet as a genshi stream
        @param include_content: Application content.
        '''
        template = self._get_template()
        context = self._get_context(include_content)
        return render_to_stream(template, context)

    def _get_context(self, include_content=None):
        '''
        Builds the context for the application
        @param include_content: Application content.
        '''
        context = super(ApplicationPagelet, self)._get_context()
        context['title'] = self.title
        if include_content is not None:
            context['content'] = include_content
        return context
    
    def json(self, process_url=None):
        '''
        Returns the content as a json object be parsed and loaded in javascript
        @param process_url: url of the application to be loaded
        '''
        if process_url is not None:
            self.process_url = process_url
        application_content = self._build_content()
        if isinstance(application_content, AMPCMSAjaxResponse):
            return application_content.response
        elif isinstance(application_content, HttpResponseFullRedirect):
            return json.dumps({C.JSON_KEY_REDIRECT: True,
                               C.JSON_KEY_NAME: self._data_model.name,
                               C.JSON_KEY_LOCATION: application_content['location'],
                               C.JSON_KEY_HTML: '',
                               C.JSON_KEY_CSS: self._build_css(),
                               C.JSON_KEY_JS: self._build_js()})
        elif isinstance(application_content, HttpResponseRedirect) or isinstance(application_content, HttpFixedResponse):
            return application_content
        else:
            html = self.html(include_content=application_content)
            return json.dumps({C.JSON_KEY_REDIRECT: False,
                               C.JSON_KEY_NAME: self._data_model.name,
                               C.JSON_KEY_LOCATION: self.process_url,
                               C.JSON_KEY_HTML: Markup(html),
                               C.JSON_KEY_CSS: self._build_css(),
                               C.JSON_KEY_JS: self._build_js(),
                               C.JSON_KEY_MESSAGES : [{'message': message.message, 'level': message.level, 'tags': message.tags} for message in messages.get_messages(self.request)]
            })
    
    def _build_content(self, process_url=None):
        '''
        Resolve starting_url to a view and make a call to that view. If receives a HttpResponseRedirect back from, use the new
        location to resolve a new view and make a call to that view.
        @param process_url: starting_url to build content based on. Will default to self.starting_url if None is passed.
        '''
        # FIXME: this is handled backwards. any process url sent in should ovewrite anything else.
        if process_url is not None and self.process_url is None and self._data_model.starting_url is not None:
            self.process_url = self._data_model.starting_url
        elif self.process_url is None:
            self.process_url = '/'
        else:
            self.process_url = self.process_url
        try:
            application = application_mapper.get_item(self._data_model.application)
            set_urlconf(application.urlconf)
            view, args, kwargs = resolve(self.process_url)
            self.request.is_ampcms = True
            response = view(self.request, *args, **kwargs)
            if isinstance(response, HttpResponseSSLRedirect):
                pagelet_params = urllib.urlencode({'%s-pagelet' % self._data_model.name: self.process_url})
                redirect_url = 'https://%s%s?%s' % (self.request.get_host(), self._data_model.page.get_absolute_url(), pagelet_params)
                return HttpResponseFullRedirect(redirect_url)
            if isinstance(response, AMPCMSAjaxResponse) or isinstance(response, HttpResponseFullRedirect) or isinstance(response, HttpFixedResponse):
                # These responses return as is
                return response
            elif isinstance(response, HttpResponseRedirect):
                log.debug('Redirecting to %s' % response['location'])
                response['location'] = '%s%s' % (self._data_model.get_absolute_url(), response['location'])
                return response
            if hasattr(response, 'ampcms_media'):
                self.view_css = response.ampcms_media.css
                self.view_js = response.ampcms_media.js
                if response.ampcms_media.title is not None:
                    self.title = response.ampcms_media.title
                else:
                    self.title = self._data_model.title
            set_urlconf(None)
            return Markup(response.content)
        except Exception, e:
            set_urlconf(None)
            log.exception('Exception loading application pagelet: %s' % e)
            resolver = get_resolver(None)
            if isinstance(e, Http404):
                self.title = settings.AMPCMS_404_TITLE
                error_view, kwargs = resolver.resolve404()
            else:
                self.title = settings.AMPCMS_500_TITLE
                error_view, kwargs = resolver.resolve500()
            kwargs['exception'] = e
            error_response = error_view(self.request, **kwargs)
            return Markup(error_response.content)

    def _get_html_data(self):
        '''
        Build the html data tags
        '''
        data = super(ApplicationPagelet, self)._get_html_data()
        data.update({C.HTML_DATA_TAG_KEY_STARTING_URL : self._data_model.starting_url if self._data_model.starting_url else '/',
                     C.HTML_DATA_TAG_KEY_LOCATION: self.process_url,
                     C.HTML_DATA_TAG_KEY_APPLICATION : self._data_model.application})
        return data

pagelet_mapper = ContentTypeMapper(BasePagelet)
pagelet_mapper.register('SimplePagelet', SimplePagelet)
pagelet_mapper.register('ApplicationPagelet', ApplicationPagelet)
