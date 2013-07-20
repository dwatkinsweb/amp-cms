from ampcms.models import Page, Pagelet, AmpCmsSite

import urllib

def build_url(site, module_name, page_name, pagelet_urls=None):
    page = Page.objects.get(name=page_name, module__name=module_name, module__site=site)
    if pagelet_urls is not None:
        pagelet_params = '?'+urllib.urlencode(pagelet_urls)
    else: 
        pagelet_params = ''
    return '%s%s' % (page.get_absolute_url(), pagelet_params)

def build_pagelet_url(request, pagelet_url):
    site = AmpCmsSite.objects.get_by_request(request)
    pagelet = Pagelet.objects.get(name=request.ampcms_pagelet.replace('-pagelet', ''),
                                  page__name=request.ampcms_page, 
                                  page__module__name=request.ampcms_module, 
                                  page__module__site=site)
    return '%s%s' % (pagelet.get_absolute_url(), pagelet_url)
    
    