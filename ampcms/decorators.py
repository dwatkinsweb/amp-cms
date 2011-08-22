from ampcms.models import Site, get_module_and_page, get_user_module_and_page
from ampcms.lib.exceptions import PageDoesNotExist
from ampcms.conf import settings
from django.utils.functional import wraps
from django.utils.decorators import available_attrs
from django.utils.http import urlquote
from django.http import HttpResponseRedirect

import logging
log = logging.getLogger(__name__)

def user_passes_test(function, login_url=settings.AMPCMS_LOGIN_URL, public_url=settings.AMPCMS_PUBLIC_URL, permission_denied_url=settings.AMPCMS_PERMISSION_DENIED_URL):
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            site = Site.objects.get_current()
            if not site.private:
                # Attempt to load module and page
                try:
                    module, page = get_module_and_page(site, kwargs.get('module'), kwargs.get('page'))
                except (PageDoesNotExist):
                    # Redirect to the public home page
                    return HttpResponseRedirect(public_url)
                else:
                    log.info('Successfully loaded module and page: User %s viewing page %s.%s' 
                              % (request.user.username, module.name, page.name))
            elif request.user.is_authenticated():
                # Attempt to load module and page
                try:
                    module, page = get_user_module_and_page(request.user, site, kwargs.get('module'), kwargs.get('page'))
                except (PageDoesNotExist):
                    return HttpResponseRedirect(permission_denied_url)
                else:
                    log.info('Successfully loaded module and page: User %s viewing page %s.%s' 
                              % (request.user.username, module.name, page.name))
            else:
                # TODO: Find a way to be able to redirect with the hash tag still available. Will require javascript.
                return HttpResponseRedirect('%s?next=%s' % (login_url, urlquote(request.get_full_path())))
            
            kwargs.update({
                'site_model': site,
                'module_model': module,
                'page_model': page
            })
            if request.user.has_acl(module, page):
                return view_func(request, *args, **kwargs)
            else:
                log.warning('User ACL rejected for %s viewing %s.%s' % (request.user, module.name, page.name))
                return HttpResponseRedirect(permission_denied_url)
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return _decorator

def acl_required(function=None, login_url=settings.AMPCMS_LOGIN_URL, public_url=settings.AMPCMS_PUBLIC_URL, permission_denied_url=settings.AMPCMS_PERMISSION_DENIED_URL):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        public_url=public_url,
        permission_denied_url=permission_denied_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator