from ampcms.models import Page

import urllib

def build_url(site, module_name, page_name, pagelet_urls=None):
    page = Page.objects.get(name=page_name, module__name=module_name, module__site=site)
    if pagelet_urls is not None:
        pagelet_params = '?'+urllib.urlencode(pagelet_urls)
    else: 
        pagelet_params = ''
    return '%s%s' % (page.get_absolute_url(), pagelet_params)