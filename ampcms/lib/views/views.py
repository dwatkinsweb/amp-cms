from django.views.generic.base import TemplateView, View
from django.http import HttpResponse
from django.template.response import TemplateResponse

from ampcms.lib.http.response import AMPCMSMedia, AMPCMSAjaxResponse
from ampcms.models import AmpCmsSite
from ampcms.conf import settings

import json

def _get_response_class():
    #FIXME: make this a module path as a string instead of an actual class
    if settings.AMPCMS_RESPONSE_CLASS is not None:
        return settings.AMPCMS_RESPONSE_CLASS
    else:
        return TemplateResponse

class AjaxResponseMixin(object):
    def dispatch(self, request, *args, **kwargs):
        return AMPCMSAjaxResponse(super(AjaxResponseMixin, self).dispatch(request, *args, **kwargs))

class AmpCmsTemplateSkinMixin(object):
    response_class = _get_response_class()
    
    def get_template_names(self):
        if not isinstance(self.template_name, list):
            template_names = [self.template_name]
        else:
            template_names = self.template_name
        site = AmpCmsSite.objects.get_by_request(self.request)
        if site.skin is not None:
            template_names.insert(0, '%s/%s' % (site.skin, self.template_name))
            template_names.insert(0, '%s/%s/%s' % (settings.AMPCMS_SKIN_FOLDER, site.skin, self.template_name))
        return template_names
    
class AmpCmsView(AmpCmsTemplateSkinMixin, TemplateView):
    pagelet_title = None
    pagelet_javascript = []
    pagelet_css = []
    
    def dispatch(self, *args, **kwargs):
        response = super(AmpCmsView, self).dispatch(*args, **kwargs)
        if hasattr(self.request, 'is_ampcms') and self.request.is_ampcms:
            site = AmpCmsSite.objects.get_by_request(self.request)
            response.ampcms_media = AMPCMSMedia(site, self.pagelet_title, self.pagelet_css, self.pagelet_javascript)
        return response
        
class AmpCmsAjaxView(AjaxResponseMixin, AmpCmsTemplateSkinMixin, TemplateView): pass

class AmpCmsJsonView(AjaxResponseMixin, View):
    def get(self, request, *args, **kwargs):
        # By default, get is handled exactly like post
        return self.post(self, request, *args, **kwargs)
    
    def get_response(self, **kwargs):
        return ''
    
    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_response(**kwargs))
    
    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **kwargs):
        return HttpResponse(content, content_type='application/json', **kwargs) 

    def convert_context_to_json(self, context):
        return json.dumps(context)