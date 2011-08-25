from django_genshi.shortcuts import render_to_stream
from django_genshi import RequestContext
from genshi.core import Markup

from ampcms import const as C
from django.core.exceptions import ImproperlyConfigured

class BaseContentType(object):
    '''
    Base Content Object to extend when creating different content types
    Built in content types are Layouts, Pages, and Pagelets
    '''
    def __init__(self, request, request_kwargs, *args, **kwargs):
        '''
        @param request: HttpRequest object sent to view
        @param request_kwargs: kwargs dictionary sent to view
        '''
        self.request = request
        self.request_kwargs = request_kwargs
        self._children = None
        self._data_model = None
        self._css = None
        self._template = None

    def children(self):
        '''
        Return a list of children that will be rendered in the template. Will build the children if not already built.
        '''
        if self._children is None:
            self._children = self._build_children()
        return self._children

    def _build_children(self):
        #TODO: maybe have this raise a NotImplementedError
        return {}

    def css(self):
        '''
        Return the css for the layout and removes any duplicate entries. Will build the css if not already built.
        TODO: Turn this into a concatenation of the files 
        '''
        if self._css is None:
            css_list = self._build_css()
            css_list_unique = []
            [css_list_unique.append(css) for css in css_list if (css and not css_list_unique.count(css))]
            self._css = '\n'.join(['@import url("%s");' % _css for _css in css_list_unique])
        return self._css
    
    def _build_css(self):
        '''
        Build the css based on the children
        '''
        css = []
        for child in self.children().values():
            css += child._build_css()
        return css
    
    def html(self):
        return self._to_stream().render()

    def markup(self):
        '''
        Return the rendered layout as an html safe object
        '''
        return Markup(self.html())
    
    def _to_stream(self):
        '''
        Convert the layout into a Genshi Stream
        '''
        template = self._get_template()
        context = self._get_context()
        return render_to_stream(template, context)
    
    def _get_template(self):
        '''
        Return the template needed for the object
        '''
        if self._template is None:
            raise ImproperlyConfigured('No template defined for object %s' % type(self))
        return self._template
    
    def _get_context(self):
        '''
        Build the context needed to html the object. Initiailzes with any jQuery/HTML5 data tags.
        '''
        if self.request is not None:
            context = RequestContext(self.request, self.request_kwargs)
        else:
            context = {}
        context.update({C.CONTENT_TYPE_CONTEXT_DATA_MODEL : self._data_model,
                        C.CONTENT_TYPE_CONTEXT_CHILDREN: self.children(),
                        C.CONTENT_TYPE_CONTEXT_HTML_DATA_TAGS : self.get_html_data_tags()})
        return context
    
    def get_html_data_tags(self):
        '''
        Convert the data into jQuery/HTML5 data tags
        '''
        return {'%s%s' % (C.HTML_DATA_TAG_PREFIX, key) : '%s' % val for key, val in self._get_html_data().items()}

    def _get_html_data(self):
        '''
        Return a dictionary of data that will be transformed into jQuery/HTML5 data tags
        '''
        #TODO: maybe have this raise a NotImplementedError
        return {}
