from ampcms.models import Page

import urllib

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def set_current_request(request):
    _thread_locals.request = request

def build_url(site, module_name, page_name, pagelet_urls):
    page = Page.objects.get(name=page_name, module__name=module_name, module__site=site)
    pagelet_params = urllib.urlencode(pagelet_urls)
    return '%s?%s' % (page.get_absolute_url(), pagelet_params)