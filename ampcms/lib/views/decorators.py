#-------------------------------------------------------------------------------
# Copyright David Watkins 2011
# 
# AMP-CMS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from ampcms.models import AmpCmsSite, get_public_module_and_page, get_private_module_and_page
from ampcms.lib.exceptions import PageDoesNotExist, NoPermissions
from ampcms.lib.http.response import AMPCMSAjaxResponse, HttpResponseSSLRedirect, AMPCMSMedia, HttpResponseFullRedirect
from ampcms.lib.api.api import build_url
from ampcms import const as C
from django.utils.functional import wraps
from django.utils.decorators import available_attrs
from django.utils.http import urlquote, urlencode
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from ampcms.conf import settings

import logging
log = logging.getLogger(__name__)

def user_has_acl(function, login_url=settings.AMPCMS_ACCOUNT_LOGIN_URL, public_url=settings.AMPCMS_PUBLIC_URL, permission_denied_url=settings.AMPCMS_PERMISSION_DENIED_URL):
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            site = AmpCmsSite.objects.get_by_request(request)
            module_name = kwargs.get(C.URL_KEY_MODULE)
            page_name = kwargs.get(C.URL_KEY_PAGE)
            if not site.private:
                try:
                    module, page = get_public_module_and_page(site, module_name, page_name, request.user)
                except:
                    # Redirect to the public home page
                    return HttpResponseRedirect(public_url)
                else:
                    if page is None and (module.redirect_url or module.redirect_module):
                        if module.redirect_url:
                            log.debug('Successfully loaded module. Redirecting to %s' % module.redirect_url)
                            return HttpResponsePermanentRedirect(module.redirect_url)
                        elif module.redirect_module is not None:
                            if request.is_secure():
                                redirect_url = 'https://%s%s?%s' % (module.redirect_module.site.domain,
                                                                    module.redirect_module.get_absolute_url(),
                                                                    request.GET.urlencode())
                            else:
                                redirect_url = 'http://%s%s?%s' % (module.redirect_module.site.domain,
                                                                   module.redirect_module.get_absolute_url(),
                                                                   request.GET.urlencode())
                            log.debug('Successfully loaded module. Redirecting to %s' % redirect_url)
                            return HttpResponsePermanentRedirect(redirect_url)
                    else:
                        log.debug('Successfully loaded module and page: User %s viewing %s and %s' 
                                  % (request.user.username, module.name, page.name))
                if page.private and not request.user.is_authenticated():
                    log.debug('Site is private and no user is logged in. Redirecting to login.')
                    return HttpResponseRedirect('%s?%s=%s' % (login_url, REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
            elif request.user.is_authenticated():
                # Attempt to load module and page
                try:
                    module, page = get_private_module_and_page(site, module_name, page_name, request.user)
                except PageDoesNotExist:
                    return HttpResponseRedirect(permission_denied_url)
                except NoPermissions:
                    return HttpResponseRedirect(settings.AMPCMS_ACCOUNT_NO_PERMISSIONS_URL)
                else:
                    log.debug('Successfully loaded module and page: User %s viewing page %s.%s' 
                              % (request.user.username, module.name, page.name))
            else:
                return HttpResponseRedirect('%s?%s=%s' % (login_url, REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
            
            kwargs.update({
                C.EXTRA_KWARGS_SITE : site,
                C.EXTRA_KWARGS_MODULE : module,
                C.EXTRA_KWARGS_PAGE : page
            })
            if not site.private or request.user.has_acl(module, page):
                return view_func(request, *args, **kwargs)
            else:
                log.warning('User ACL rejected for %s viewing %s.%s' % (request.user, module.name, page.name))
                return HttpResponseRedirect(permission_denied_url)
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return _decorator

def acl_required(function=None, login_url=settings.AMPCMS_ACCOUNT_LOGIN_URL, public_url=settings.AMPCMS_PUBLIC_URL, permission_denied_url=settings.AMPCMS_PERMISSION_DENIED_URL):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_has_acl(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        public_url=public_url,
        permission_denied_url=permission_denied_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def ampcms_view(title=None, css_files=[], js_files=[], ssl_required=False):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if hasattr(request, 'is_ampcms') and request.is_ampcms:
                if ssl_required and not request.is_secure():
                    return HttpResponseSSLRedirect()
            response = view_func(request, *args, **kwargs)
            # Only apply changes if coming from ampcms
            if hasattr(request, 'is_ampcms') and request.is_ampcms:
                site = AmpCmsSite.objects.get_by_request(request)
                response.ampcms_media = AMPCMSMedia(site, title, css_files, js_files)
            return response
        return wraps(view_func)(wrapped_view)
    return decorator

def ampcms_ajax_view(view_func):
    def wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response = AMPCMSAjaxResponse(response)
        return response
    return wraps(view_func)(wrapped_view)


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, **query_kwargs):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    if not login_url:
        login_url = settings.AMPCMS_ACCOUNT_LOGIN_URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            
            site = AmpCmsSite.objects.get_by_request(request)
            continue_url = build_url(site=site,
                                     module_name=request.ampcms_module,
                                     page_name=request.ampcms_page,
                                     pagelet_urls={request.ampcms_pagelet: request.ampcms_pagelet_path})

            continue_url = continue_url
            query_kwargs[redirect_field_name] = continue_url
            return HttpResponseFullRedirect('%s?%s' % (login_url, urlencode(query_kwargs)))
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, **query_kwargs):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        redirect_field_name=redirect_field_name,
        **query_kwargs
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def permission_required(perm, login_url=None):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    """
    return user_passes_test(lambda u: u.has_perm(perm), login_url=login_url)

def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if request.is_ampcms:
                return HttpResponseSSLRedirect()
            else:
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
