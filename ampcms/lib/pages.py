from django.utils.datastructures import SortedDict

from content_type import BaseContentType
from content_type_mapper import ContentTypeMapper
import pagelets

class BasePage(BaseContentType):
    '''
    Base Page object to extend when creating different types of pages
    '''
    def __init__(self, page, *args, **kwargs):
        '''
        Initialize the Base Page object
        @param page_model: page instance from the page model
        '''
        super(BasePage, self).__init__(*args, **kwargs)
        self._data_model = page
        self._template = 'page'
    
    def _get_html_data(self):
        data = {'url' : self.get_absolute_url(),
                'name' : self._data_model.name}
        return data
    
    def get_absolute_url(self):
        '''
        Get the absolute url for the page based on the page model. Will return /<module>/<page>
        '''
        return self._data_model.get_absolute_url()

class PageletPage(BasePage):
    def get_pagelet(self, pagelet=None):
        '''
        Return a pagelet based on name. If no name is given, return the first pagelet in the list.
        @param pagelet: name of pagelet
        '''
        children = self.children()
        if pagelet is not None:
            # TODO: Not sure what want to do when not found, maybe raise an exception? currently returns none.
            pagelet = children.get(pagelet)
        else:
            pagelet = children.itervalues().next()
        return pagelet
    
    def _build_children(self):
        '''
        Builds the children for the page. Cycles through the children in self.page instance and returns a dictionary
        in the structure {<pagelet.name>:<pagelet>, ...}
        '''
        _pagelets = SortedDict()
        for pagelet in self._data_model.active_pagelets():
            pagelet_class = pagelets.pagelet_mapper.get_item(pagelet.pagelet_class)
            _pagelets[pagelet.name] = pagelet_class(request=self.request, request_kwargs=self.request_kwargs, pagelet=pagelet)
        return _pagelets

page_mapper = ContentTypeMapper(BasePage)
page_mapper.register('PageletPage', PageletPage)