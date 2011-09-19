from genshi.core import Markup
from django_genshi.shortcuts import render_to_stream
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import resolve

from ampcms.lib.content_type import BaseContentType
from ampcms.lib.content_type_mapper import ContentTypeMapper
from ampcms.lib.application_mapper import application_mapper
from ampcms import const as C

import json

import logging
log = logging.getLogger(__name__)

class BasePagelet(BaseContentType):
    '''
    Base pagelet object for all pagelets to extend.
    This contains the base functionality for generating content, css, and js for the pagelets.
    Only methods that should need to be overwritten are _get_context and _get_template.
    Will look in /pagelets folder when grabbing media and templates
    '''
    def __init__(self, pagelet=None, template='ampcms/pagelets/base.html', **kwargs):
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
        css = self._data_model.css_files
        if css is not None and not isinstance(css, list):
            css = [val.strip() for val in css.split(',')]
        else:
            css = []
        css += self.view_css
        return filter(None, css)
    
    def _build_js(self):
        '''
        Build the js based on any pagelet attributes
        '''
        js = self._data_model.js_files
        if js is not None and not isinstance(js, list):
            js = [val.strip() for val in js.split(',')]
        else:
            js = []
        js += self.view_js
        return filter(None, js)

class MenuPagelet(BasePagelet):
    '''
    Pagelet used to build a menu. This is not a pagelet that 
    '''
    def __init__(self, menu_label=None, selected_item=None, template='ampcms/pagelets/menu.html', pagelet=None, **kwargs):
        '''
        Initialize the menu. Default this pagelet to None because the pagelet may not be created from the database.
        @param menu_label: label of the menu used as the <ul> class and id
        @param selected_item: selected menu item will be flagged with a class of selected
        @param template: list of menu children. Each item needs to be in a tuple(label, href) format
        '''
        super(MenuPagelet, self).__init__(**kwargs)
        self.menu_label = menu_label
        self.selected_item = selected_item
        self._template = template
        self._children = []
    
    def append(self, label, href):
        '''
        Manually append a new item to the menu
        @param label: label to be display for the menu
        @param href: url for the menu item
        '''
        self._children.append((label,href))
    
    def _get_context(self):
        context = super(MenuPagelet, self)._get_context()
        context.update({C.CONTENT_TYPE_CONTEXT_MENU_LABEL: self.menu_label,
                        C.CONTENT_TYPE_CONTEXT_SELECTED_ITEM : self.selected_item})
        return context
    
    def _get_html_data(self):
        data = {C.HTML_DATA_TAG_KEY_NAME : self.menu_label}
        return data
    
    def _build_css(self):
        '''
        Return the css based on the menu_label
        '''
        return ['%scss/%s.css' % (settings.MEDIA_URL, self.menu_label)]

class SimplePagelet(BasePagelet):
    '''
    Simple container that displays a small bit of html output
    '''
    def __init__(self, template='ampcms/pagelets/simple.html', **kwargs):
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
    def __init__(self, template='ampcms/pagelets/application.html', **kwargs):
        super(ApplicationPagelet, self).__init__(**kwargs)
        self._template = template
        self.process_url = None
        
    def html(self, include_content=False):
        return self._to_stream(include_content).render()

    def _to_stream(self, include_content=False):
        '''
        Renders the pagelet as a genshi stream
        @param include_content: Whether or not to load the application content. By default, just renders the frame.
        '''
        template = self._get_template()
        context = self._get_context(include_content)
        return render_to_stream(template, context)

    def _get_context(self, include_content=False):
        '''
        Builds the context for the application
        @param include_content: Whether or not to load the application content. By default, just renders the frame.
        '''
        context = super(ApplicationPagelet, self)._get_context()
        if include_content:
            context['content'] = self._build_content()
        return context
    
    def json(self, process_url=None):
        '''
        Returns the content as a json object be parsed and loaded in javascript
        @param process_url: url of the application to be loaded
        '''
        # TODO: there needs to be a way for methods to be able to return their response as is.
        if process_url is not None:
            self.process_url = process_url
        html = self.html(include_content=True)
        return json.dumps({C.JSON_KEY_NAME: self._data_model.name,
                           C.JSON_KEY_LOCATION: self.process_url,
                           C.JSON_KEY_HTML: Markup(html),
                           C.JSON_KEY_CSS: self._build_css(),
                           C.JSON_KEY_JS: self._build_js(),
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
            view, args, kwargs = resolve(self.process_url, application.urlconf)
            self.request.is_ampcms = True
            response = view(self.request, *args, **kwargs)
            if isinstance(response, HttpResponseRedirect):
                # TODO: I don't like the way this is removing the prefix out of the url but couldn't think of anything better atm.
                self.process_url = response['location'].replace('/%s' % application.url_prefix, '', 1)
                return self._build_content()
            if hasattr(response, 'ampcms_media'):
                self.view_css = response.ampcms_media.css
                self.view_js = response.ampcms_media.js
            return Markup(response.content)
        except Exception, e:
            log.exception('Exception loading application pagelet: %s' % e)
            raise

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