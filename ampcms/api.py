from ampcms.models import Page

import urllib

def build_url(site, module_name, page_name, pagelet_urls):
    page = Page.objects.get(name=page_name, module__name=module_name, module__site=site)
    pagelet_params = urllib.urlencode(pagelet_urls)
    return '%s?%s' % (page.get_absolute_url(), pagelet_params)