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

from django.db.models import Q
from django.db.models import Manager
from django.contrib.sites.models import SiteManager as DjangoSiteManager

from ampcms.conf import settings

import logging
log = logging.getLogger(__name__)

class ModuleManager(Manager):
    use_for_related_fields = True
    
    def active(self):
        active_pagelets = self.get_query_set().filter(active=True)
        if settings.AMPCMS_CACHING:
            active_pagelets.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return active_pagelets
    
    def active_site_modules(self, site):
        '''
        Get active modules for a given site.
        @param site: AmpCms Site Model instance
        '''
        modules = self.active().filter(site=site).distinct()
        if settings.AMPCMS_CACHING:
            modules.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return modules
    
    def active_user_site_modules(self, user, site):
        '''
        Get the active modules for a given user and site.
        @param user: AmpCms User Model instance
        @param site: AmpCms Site Model instance
        '''
        # Have to import here or causes an import error in from middleware
        from ampcms.models import Page
        if user.is_superuser:
            user_site_pages = Page.objects.filter(module__site=site)
        else:
            user_site_pages = Page.objects.active_user_pages(user).filter(module__site=site)
        modules = self.active_site_modules(site).filter(pages__in=user_site_pages).distinct()
        if settings.AMPCMS_CACHING:
            modules.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return modules
    
    def get_by_natural_key(self, name, site_name, site_domain):
        return self.get(name=name, site__name=site_name, site__domain=site_domain)

class PageManager(Manager):
    use_for_related_fields = True
    
    def active(self):
        pages = self.get_query_set().filter(active=True).distinct()
        if settings.AMPCMS_CACHING:
            pages.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return pages
    
    def active_user_pages(self, user):
        pages = self.active()
        if not user.is_superuser:
            pages = pages.filter(Q(user=user) | Q(group__user=user))
        if settings.AMPCMS_CACHING:
            pages.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return pages

    def active_module_pages(self, user, module):
        pages = self.active().filter(module=module)
        if user.is_authenticated():
            pages = pages.filter(Q(private=False) | Q(user=user) | Q(group__user=user))
        if settings.AMPCMS_CACHING:
            pages.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return pages
    
    def active_user_module_pages(self, user, module):
        pages = self.active_module_pages(user, module)
        if not user.is_superuser:
            pages = pages.filter(Q(user=user) | Q(group__user=user))
        pages = pages.distinct()
        if settings.AMPCMS_CACHING:
            pages.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return pages
    
    def get_by_natural_key(self, name, module_name, site_name, site_domain):
        return self.get(name=name, module__name=module_name, module__site__name=site_name, module__site__domain=site_domain)

class PageletManager(Manager):
    use_for_related_fields = True
    
    def active(self):
        active_pagelets = self.get_query_set().filter(active=True)
        if settings.AMPCMS_CACHING:
            active_pagelets.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return active_pagelets
    
    def active_user_page_pagelets(self, user, page):
        user_page_pagelets = self.active().filter(page=page)
        if not user.is_superuser:
            user_page_pagelets = user_page_pagelets.filter(Q(user=user) | Q(group__user=user))
        user_page_pagelets = user_page_pagelets.distinct()
        if settings.AMPCMS_CACHING:
            user_page_pagelets.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return user_page_pagelets
    
    def get_by_natural_key(self, name, page_name, module_name, site_name, site_domain):
        return self.get(name=name, page__name=page_name, page__module__name=module_name, page__module__site__name=site_name, page__module__site__domain=site_domain)

class SiteManager(DjangoSiteManager):
    def get_by_request(self, request):
        if request is None:
            return self.get_current()
        host = request.get_host()
        current_site = self.get_query_set().filter(domain=host)
        if settings.AMPCMS_CACHING:
            current_site.cache(timeout=settings.AMPCMS_CACHING_TIMEOUT)
        return current_site[0]
    
    def get_by_natural_key(self, name, domain):
        return self.get(name=name, domain=domain)

if settings.AMPCMS_CACHING:
    from caching.base import CachingManager #@UnresolvedImport
    SiteManager.__bases__ += (CachingManager,)
    ModuleManager.__bases__ = (CachingManager,)
    PageManager.__bases__ = (CachingManager,)
    PageletManager.__bases__ = (CachingManager,)
