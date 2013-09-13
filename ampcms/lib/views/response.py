from django.template.response import TemplateResponse
from django_genshi import Context, RequestContext
from django_genshi import loader as genshi_loader
from django_genshi.shortcuts import _get_filters

class AmpCmsResponse(object): pass

class AmpCmsTemplateResponse(TemplateResponse): pass

class AmpCmsDjangoResponse(AmpCmsResponse, AmpCmsTemplateResponse): pass

class AmpCmsGenshiResponse(AmpCmsResponse, AmpCmsTemplateResponse):
    def resolve_template(self, template):
        """Accepts a template object, path-to-template or list of paths"""
        if isinstance(template, (list, tuple)):
            return genshi_loader.select_template(template)
        elif isinstance(template, basestring):
            return genshi_loader.get_template(template)
        else:
            return template
        
    def resolve_context(self, context):
        """Convert context data into a full RequestContext object
        (assuming it isn't already a Context object).
        """
        if isinstance(context, Context):
            return context
        return RequestContext(self._request, context)
    
    @property
    def rendered_content(self):
        """Returns the freshly rendered content for the template and context
        described by the TemplateResponse.

        This *does not* set the final content of the response. To set the
        response content, you must either call render(), or set the
        content explicitly using the value of this property.
        """
        from ampcms.conf import settings
        template = self.resolve_template(self.template_name)
        context = self.resolve_context(self.context_data)
        stream = template.generate(context)
        filtered = stream.filter (*_get_filters())
        content = filtered.render('html', encoding=settings.DEFAULT_CHARSET, strip_whitespace=False)
        return content