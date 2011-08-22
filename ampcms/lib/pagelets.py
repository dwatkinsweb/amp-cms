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

class BasePagelet(BaseContentType):
    '''
    Base pagelet object for all pagelets to extend.
    This contains the base functionality for generating content, css, and js for the pagelets.
    Only methods that should need to be overwritten are _get_context and _get_template.
    Will look in /pagelets folder when grabbing media and templates
    '''
    def __init__(self, pagelet=None, template='pagelets/base', **kwargs):
        '''
        @param pagelet: pagelet instance from the pagelet model
        @param template: name of the template
        @param classes: any other css classes to add to pagelet
        '''
        super(BasePagelet, self).__init__(**kwargs)
        self._data_model = pagelet
        self._template = template
    
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
        return css
    
    def _build_js(self):
        '''
        Build the js based on any pagelet attributes
        '''
        js = self._data_model.js_files
        if js is not None and not isinstance(js, list):
            js = [val.strip() for val in js.split(',')]
        else:
            js = []
        return js

class MenuPagelet(BasePagelet):
    '''
    Pagelet used to build a menu. This is not a pagelet that 
    '''
    def __init__(self, menu_label=None, selected_item=None, template='pagelets/menu', pagelet=None, **kwargs):
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
        return ['%scss/%s.css' % (settings.AMPCMS_MEDIA_URL, self.menu_label)]

class SimplePagelet(BasePagelet):
    '''
    Simple container that displays a small bit of html output
    '''
    def __init__(self, template='pagelets/simple', **kwargs):
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
    def __init__(self, template='pagelets/application', **kwargs):
        super(ApplicationPagelet, self).__init__(**kwargs)
        self._template = template
        self.process_url = None
        
    def html(self, include_content=False):
        return self._to_stream(include_content).render()

    def _to_stream(self, include_content=False):
        '''
        Convert the layout into a Genshi Stream
        '''
        template = self._get_template()
        context = self._get_context(include_content)
        return render_to_stream(template, context)

    def _get_context(self, include_content=False):
        context = super(ApplicationPagelet, self)._get_context()
        if include_content:
            context['content'] = self._build_content()
        return context
    
    def json(self, process_url=None):
        if process_url is not None:
            self.process_url = process_url
        html = self.html(include_content=True)
        return json.dumps({C.JSON_KEY_LOCATION: self.process_url,
                           C.JSON_KEY_HTML: Markup(html),
                           C.JSON_KEY_CSS: self._build_css(),
                           C.JSON_KEY_JS: self._build_js(),
                           })
    
    def _build_content(self):
        '''
        Resolve starting_url to a view and make a call to that view. If receives a HttpResponseRedirect back from, use the new
        location to resolve a new view and make a call to that view.
        @param starting_url: starting_url to build content based on. Will default to self.starting_url if None is passed.
        '''
        if self.process_url is None and self._data_model.starting_url is not None:
            self.process_url = self._data_model.starting_url
        elif self.process_url is None:
            self.process_url = '/'
        else:
            self.process_url = self.process_url
        urlconf = application_mapper.get_item(self._data_model.application).urlconf
        view, args, kwargs = resolve(self.process_url, urlconf)
        content = view(self.request, *args, **kwargs)
        if isinstance(content, HttpResponseRedirect):
            self.process_url = content['location']
            return self._build_content(content['location'])
        return Markup(content.content)

    def _get_html_data(self):
        data = super(ApplicationPagelet, self)._get_html_data()
        data.update({C.HTML_DATA_TAG_KEY_STARTING_URL : self._data_model.starting_url if self._data_model.starting_url else '/',
                     C.HTML_DATA_TAG_KEY_APPLICATION : self._data_model.application})
        return data

pagelet_mapper = ContentTypeMapper(BasePagelet)
pagelet_mapper.register('SimplePagelet', SimplePagelet)
pagelet_mapper.register('ApplicationPagelet', ApplicationPagelet)