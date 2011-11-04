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

from django.db import models  
from django.contrib.auth.models import User as DjangoUser, Group as DjangoGroup
from django.contrib.sites.models import Site as DjangoSite

from ampcms import managers
from ampcms.lib.exceptions import PageDoesNotExist
from ampcms.lib.pages import page_mapper
from ampcms.lib.pagelets import pagelet_mapper
from ampcms.lib.application_mapper import application_mapper
from ampcms.conf import settings

import logging
log = logging.getLogger(__name__)

application_mapper.autodiscover()

class Site(DjangoSite):
    private = models.BooleanField()
    skin = models.CharField(max_length=20, null=True, blank=True)

    objects = managers.SiteManager()

class Module(models.Model):
    name = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=30)
    order = models.IntegerField(max_length=2, unique=True)
    active = models.BooleanField(default=False)
    site = models.ForeignKey(Site)

    objects = managers.ModuleManager()

    def save(self, *args, **kwargs):
        if self.order is None:
            try:
                last = Module.objects.order_by('-order')[0]
                self.order = last.order + 1
            except:
                self.order = 1
        return super(Module, self).save(*args, **kwargs)
    
    @property
    def active_pages(self):
        return self.pages.filter(active=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['order']

class Page(models.Model):
    # TODO: Allow for a many to many relationship between page and pagelet
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    page_class = models.CharField(max_length=30, choices=[(page_name, page_name) for page_name, page in page_mapper.items])
    application = models.CharField(max_length=30, blank=True, null=True,
                                   choices=[(application_name, application_name) for application_name, application in application_mapper.items])
    order = models.IntegerField()
    active = models.BooleanField(default=False)
    module = models.ForeignKey(Module, related_name='pages')
    pagelet_layout = models.CharField(max_length=30, blank=True, null=True,
                                      choices=[(layout, layout) for layout in settings.AMPCMS_PAGELET_LAYOUTS])
    
    objects = managers.PageManager()
    
    def get_absolute_url(self):
        return '/%s/%s' % (self.module.name, self.name)
    
    def __unicode__(self):
        return '%s.%s' % (self.module.name, self.name)
    
    class Meta:
        ordering = ['module__order', 'order']
        unique_together = (('module', 'name'), ('module', 'order'))

class Pagelet(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    pagelet_class = models.CharField(max_length=30, choices=[(pagelet_name, pagelet_name) for pagelet_name, pagelet in pagelet_mapper.items])
    application = models.CharField(max_length=30, blank=True, null=True,
                                   choices=[(application_name, application_name) for application_name, application in application_mapper.items])
    starting_url = models.CharField(max_length=50, blank=True, null=True)
    css_files = models.CharField(max_length=255, blank=True, null=True)
    js_files = models.CharField(max_length=255, blank=True, null=True)
    classes = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    active = models.BooleanField(default=False)
    page = models.ForeignKey(Page, related_name='pagelets')
    
    objects = managers.PageletManager()
    
    def get_absolute_url(self):
        return '/pagelet/%s/%s/%s' % (self.page.module.name, self.page.name, self.name)
    
    def __unicode__(self):
        return '%s.%s.%s' % (self.page.module.name, self.page.name, self.name)
    
    class Meta:
        ordering = ['page__module__order', 'page__order', 'order']
        unique_together = (('page', 'name'), ('page', 'order'))

class PageletAttribute(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=100)
    pagelet = models.ForeignKey(Pagelet, related_name='attributes')
    
    def __unicode__(self):
        return '%s.%s.%s - %s=%s' % (self.pagelet.page.module.name, self.pagelet.page.name, self.pagelet.name, 
                                     self.name, self.value)
    
    class Meta:
        ordering = ['name']
        unique_together = (('pagelet', 'name'))

class Group(DjangoGroup):
    acl_pages = models.ManyToManyField(Page, blank=True)
    acl_pagelets = models.ManyToManyField(Pagelet, blank=True)

class User(DjangoUser):
    acl_pages = models.ManyToManyField(Page, blank=True)
    acl_pagelets = models.ManyToManyField(Pagelet, blank=True)
    
    def has_acl(self, module, page):
        return self.has_perm('%s.%s' % (module.name, page.name))

if settings.AMPCMS_CACHING:
    from caching.base import CachingMixin
    Site.__bases__ += (CachingMixin,)
    Module.__bases__ += (CachingMixin,)
    Page.__bases__ += (CachingMixin,)
    Pagelet.__bases__ += (CachingMixin,)
    PageletAttribute.__bases__ += (CachingMixin,)
    User.__bases__ += (CachingMixin,)
    
def get_module_and_page(site, module_name, page_name):
    ''' Get the module and the page based on request/url '''
    if site.private:
        # Private sites should never use this function, raise exception and die as a safety measure
        msg = 'Private site was somehow used publicly. (%s/%s/%s)' % (site, module_name, page_name)
        log.critical(msg)
        raise Exception(msg)
    
    try:
        if module_name is None:
            try:
                page = Page.objects.active_site_pages(site)[0]
            except IndexError, e:
                msg = 'Site %s has no pages' % site
                log.warning(msg)
                raise PageDoesNotExist(msg)
            else:
                module = page.module
        else:
            module = Module.objects.active().get(name=module_name, site=site)
            if page_name is None:
                try:
                    page = Page.objects.active(site, module)[0]
                except IndexError, e:
                    msg = 'Unable to find default page for module %s on site %s' % (site, module.name)
                    log.info(msg)
                    raise PageDoesNotExist(msg)
            else:
                page = module.active_pages.get(name=page_name)
    except Module.DoesNotExist, e:
        log.warning('Module %s does not exist' % (module_name))
        raise PageDoesNotExist(e)
    except Page.DoesNotExist, e:
        log.warning('Page %s does not exist in module %s' % (page_name, module_name))
        raise PageDoesNotExist(e)
    
    return (module, page)
    
def get_user_module_and_page(user, site, module_name, page_name):
    ''' Get the module and the page based on request/url '''
    try:
        if module_name is None:
            try:
                page = Page.objects.active_user_site_pages(user, site)[0]
            except IndexError, e:
                log.info('Unable to get default page and module for user %s' % user)
                raise PageDoesNotExist('Unable to get default page and module for user %s' % user)
            else:
                module = page.module
        else:
            module = Module.objects.active_site_modules(site).get(name=module_name)
            if page_name is None:
                try:
                    page = Page.objects.active_user_site_pages(user, site, module)[0]
                except IndexError, e:
                    log.info('Unable to get default page in module %s for user %s' 
                              % (module.name, user))
                    raise PageDoesNotExist('Unable to get default page in module %s for user %s' 
                                           % (module.name, user))
            else:
                page = module.active_pages.get(name=page_name)
    except Module.DoesNotExist, e:
        log.warning('Module %s does not exist for user %s' % (module_name, user))
        raise PageDoesNotExist(e)
    except Page.DoesNotExist, e:
        log.warning('Page %s does not exist in module %s for user %s' % (page_name, module_name, user))
        raise PageDoesNotExist(e)
    
    return (module, page)
