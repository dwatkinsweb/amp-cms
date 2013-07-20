try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

from django import template

_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def set_current_request(request):
    _thread_locals.request = request

def template_exists(template_name):
    try:
        template.loader.get_template(template_name)
        return True
    except template.TemplateDoesNotExist:
        return False

def skin_template(template_name, request=None):
    if request is not None:
        from ampcms.models import AmpCmsSite
        site = AmpCmsSite.objects.get_by_request(request)
        if site.skin is not None:
            skin_template = '%s/%s' % (site.skin, template_name)
            if template_exists(skin_template):
                template_name = skin_template
    return template_name