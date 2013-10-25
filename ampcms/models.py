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
import logging

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.db.utils import DatabaseError
from django.contrib.auth.models import User as DjangoUser, Group as DjangoGroup
from django.contrib.sites.models import Site as DjangoSite
from ampcms import managers
from ampcms.lib.exceptions import PageDoesNotExist, NoPermissions
from ampcms.lib.content_type.pages import page_mapper
from ampcms.lib.content_type.pagelets import pagelet_mapper
from ampcms.lib.application.mapper import application_mapper
from ampcms.conf import settings
from django.utils import translation

log = logging.getLogger(__name__)

application_mapper.autodiscover()

class AmpCmsSite(DjangoSite):
    private = models.BooleanField()
    skin = models.CharField(max_length=20, null=True, blank=True)

    objects = managers.SiteManager()

    class Meta:
        db_table = 'ampcms_site'

    def natural_key(self):
        return (self.name, self.domain)

class Module(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='images/icons/', max_length=1024, null=True, blank=True)
    redirect_module = models.ForeignKey('self', null=True, blank=True, default=None)
    redirect_url = models.URLField(null=True, blank=True, default=None)
    order = models.IntegerField(max_length=2)
    active = models.BooleanField(default=False)
    show_in_navigation = models.BooleanField(default=True)
    site = models.ForeignKey(AmpCmsSite)

    objects = managers.ModuleManager()

    def __init__(self, *args, **kwargs):
        self._current_details = None
        super(Module, self).__init__(*args, **kwargs)

    @property
    def current_details(self):
        if self._current_details is None:
            language = translation.get_language()
            try:
                self._current_details = self.details.get(language=language)
            except ModuleDetails.DoesNotExist:
                try:
                    self._current_details = self.details.get(language=settings.LANGUAGE_CODE)
                except ModuleDetails.DoesNotExist:
                    self._current_details = self.details.all()[0]
        return self._current_details

    @property
    def active_pages(self):
        return self.pages.filter(active=True)

    @property
    def title(self):
        return self.current_details.title

    def save(self, *args, **kwargs):
        if self.order is None:
            try:
                last = Module.objects.order_by('-order')[0]
                self.order = last.order + 1
            except:
                self.order = 1
        return super(Module, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.name,) + self.site.natural_key()
    natural_key.dependencies = ['ampcms.ampcmssite']

    def get_absolute_url(self):
        return '/%s' % self.name

    def __unicode__(self):
        return '%s/%s' % (self.site, self.name)

    class Meta:
        unique_together = (('name', 'site'), ('site', 'order'))
        ordering = ['site', 'order']

class ModuleDetails(models.Model):
    module = models.ForeignKey(Module, related_name='details')
    language = models.CharField(max_length=8)
    title = models.CharField(max_length=30)

    class Meta:
        unique_together = ('module', 'language')

    def __unicode__(self):
        return u'%s: %s' % (self.module, self.language)

class Page(models.Model):
    # TODO: Allow for a many to many relationship between page and pagelet
    name = models.CharField(max_length=30)
    icon = models.ImageField(upload_to='images/icons/', max_length=1024, null=True, blank=True)
    private = models.BooleanField(default=False)
    page_class = models.CharField(max_length=30,
                                  choices=[(page_name, page_name) for page_name, page in page_mapper.items()])
    order = models.IntegerField()
    active = models.BooleanField(default=False)
    show_in_navigation = models.BooleanField(default=True)
    module = models.ForeignKey(Module, related_name='pages')
    pagelet_layout = models.CharField(max_length=30, blank=True, null=True,
                                      choices=[(layout, layout) for layout in settings.AMPCMS_PAGELET_LAYOUTS])

    objects = managers.PageManager()

    def __init__(self, *args, **kwargs):
        self._current_details = None
        super(Page, self).__init__(*args, **kwargs)

    @property
    def current_details(self):
        if self._current_details is None:
            language = translation.get_language()
            try:
                self._current_details = self.details.get(language=language)
            except PageDetails.DoesNotExist:
                try:
                    self._current_details = self.details.get(language=settings.LANGUAGE_CODE)
                except PageDetails.DoesNotExist:
                    self._current_details = self.details.all()[0]
        return self._current_details

    @property
    def title(self):
        return self.current_details.title

    def get_absolute_url(self):
        return '/%s/%s' % (self.module.name, self.name)

    def natural_key(self):
        return (self.name,) + self.module.natural_key()
    natural_key.dependencies = ['ampcms.module']

    def admin_link(self):
        if self.pk:
            admin_link = reverse('admin:ampcms_page_change', args=(self.pk,))
            return u'<a href="%s">Edit Page</a>' % admin_link
        else:
            return u''
    admin_link.allow_tags = True
    admin_link.short_description = ''

    def __unicode__(self):
        return '%s/%s' % (self.module, self.name)

    class Meta:
        ordering = ['module__site', 'module__order', 'order']
        unique_together = (('module', 'name'), ('module', 'order'))

class PageDetails(models.Model):
    page = models.ForeignKey(Page, related_name='details')
    language = models.CharField(max_length=8)
    title = models.CharField(max_length=30)

    class Meta:
        unique_together = ('page', 'language')

class Pagelet(models.Model):
    name = models.CharField(max_length=30)
    pagelet_class = models.CharField(max_length=30, choices=[(pagelet_name, pagelet_name) for pagelet_name, pagelet in
                                                             pagelet_mapper.items()])
    application = models.CharField(max_length=30, blank=True, null=True,
                                   choices=[(application_name, application_name) for application_name, application in
                                            application_mapper.items()])
    starting_url = models.CharField(max_length=50, blank=True, null=True)
    classes = models.CharField(max_length=50, blank=True, null=True)
    private = models.BooleanField(default=False)
    order = models.IntegerField()
    active = models.BooleanField(default=False)
    page = models.ForeignKey(Page, related_name='pagelets')

    objects = managers.PageletManager()

    def __init__(self, *args, **kwargs):
        self._current_details = None
        super(Pagelet, self).__init__(*args, **kwargs)

    @property
    def current_details(self):
        if self._current_details is None:
            language = translation.get_language()
            try:
                self._current_details = self.details.get(language=language)
            except PageletDetails.DoesNotExist:
                try:
                    self._current_details = self.details.get(language=settings.LANGUAGE_CODE)
                except PageletDetails.DoesNotExist:
                    self._current_details = self.details.all()[0]
        return self._current_details

    @property
    def title(self):
        return self.current_details.title

    @property
    def content(self):
        return self.current_details.content

    def get_absolute_url(self):
        return '/pagelet/%s/%s/%s' % (self.page.module.name, self.page.name, self.name)

    def natural_key(self):
        return (self.name,) + self.page.natural_key()
    natural_key.dependencies = ['ampcms.page']

    def admin_link(self):
        if self.pk:
            admin_link = reverse('admin:ampcms_pagelet_change', args=(self.pk,))
            return u'<a href="%s">Edit Pagelet</a>' % admin_link
        else:
            return u''
    admin_link.allow_tags = True
    admin_link.short_description = ''

    def __unicode__(self):
        return '%s/%s' % (self.page, self.name)

    class Meta:
        ordering = ['page__module__site', 'page__module__order', 'page__order', 'order']
        unique_together = (('page', 'name'), ('page', 'order'))

class PageletDetails(models.Model):
    pagelet = models.ForeignKey(Pagelet, related_name='details')
    language = models.CharField(max_length=8)
    title = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('pagelet', 'language')

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

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def natural_key(self):
        return (self.name,)

class User(DjangoUser):
    acl_pages = models.ManyToManyField(Page, blank=True)
    acl_pagelets = models.ManyToManyField(Pagelet, blank=True)

    def has_acl(self, module, page):
        return self.has_perm('%s.%s' % (module.name, page.name))

if settings.AMPCMS_CACHING:
    from caching.base import CachingMixin

    AmpCmsSite.__bases__ += (CachingMixin,)
    Module.__bases__ += (CachingMixin,)
    Page.__bases__ += (CachingMixin,)
    Pagelet.__bases__ += (CachingMixin,)
    PageletAttribute.__bases__ += (CachingMixin,)
    User.__bases__ += (CachingMixin,)

def get_public_module_and_page(site, module_name, page_name, user):
    ''' Get the module and the page based on request/url '''
    if site.private:
        # Private sites should never use this function, raise exception and die as a safety measure
        message = 'Private site was somehow used publicly. (%s/%s/%s)' % (site, module_name, page_name)
        log.critical(message)
        raise Exception(message)

    try:
        if module_name is None:
            try:
                page = Page.objects.active().filter(module__site=site)
                if user.is_anonymous():
                    page = page.filter(private=False)[0]
                else:
                    page = page.filter(Q(private=False) | Q(user=user) | Q(group__user=user))[0]
            except IndexError, e:
                message = 'Site %s has no pages' % site
                log.warning(message)
                raise PageDoesNotExist(message)
            else:
                module = page.module
        else:
            module = Module.objects.active().get(name=module_name, site=site)
            if module.redirect_url or module.redirect_module is not None:
                return (module, None)
            if page_name is None:
                try:
                    page = Page.objects.active_module_pages(user, module)[0]
                except IndexError, e:
                    message = 'Unable to find default page for module %s on site %s' % (site, module.name)
                    log.warning(message)
                    raise PageDoesNotExist(message)
            else:
                page = module.active_pages.get(name=page_name)
    except Module.DoesNotExist, e:
        log.warning('Module %s does not exist' % (module_name))
        raise PageDoesNotExist(e)
    except Page.DoesNotExist, e:
        log.warning('Page %s does not exist in module %s' % (page_name, module_name))
        raise PageDoesNotExist(e)

    return (module, page)

def get_private_module_and_page(site, module_name, page_name, user):
    ''' Get the module and the page based on request/url '''
    try:
        if module_name is None:
            try:
                page = Page.objects.active_user_pages(user).filter(module__site=site)[0]
            except IndexError, e:
                message = 'Unable to get default page and module for user %s' % user
                log.warning(message)
                raise NoPermissions(message)
            else:
                module = page.module
        else:
            module = Module.objects.active_user_site_modules(user, site).get(name=module_name)
            if page_name is None:
                try:
                    page = Page.objects.active_user_module_pages(user, module)[0]
                except IndexError, e:
                    message = 'Unable to get default page in module %s for user %s' % (module.name, user)
                    log.warning(message)
                    raise PageDoesNotExist(message)
            else:
                page = module.active_pages.get(name=page_name)
    except Module.DoesNotExist, e:
        log.warning('Module %s does not exist for user %s' % (module_name, user))
        raise PageDoesNotExist(e)
    except Page.DoesNotExist, e:
        log.warning('Page %s does not exist in module %s for user %s' % (page_name, module_name, user))
        raise PageDoesNotExist(e)

    return (module, page)

def create_ampcms_user(sender, instance, created, **kwargs):
    try:
        if created:
            user, user_created = (User.objects.using(instance._state.db)
                                  .get_or_create(pk=instance.id,
                                                 defaults={
                                                     'username': instance.username,
                                                     'first_name': instance.first_name,
                                                     'last_name': instance.last_name,
                                                     'email': instance.email,
                                                     'password': instance.password,
                                                     'is_staff': instance.is_staff,
                                                     'is_active': instance.is_active,
                                                     'is_superuser': instance.is_superuser,
                                                     'last_login': instance.last_login,
                                                     'date_joined': instance.date_joined}))
    except DatabaseError:
        log.warning('Unable to automatically create ampcms user post_save django_auth.user: %s' % instance)

def create_ampcms_group(sender, instance, created, **kwargs):
    try:
        if created:
            group, group_created = (Group.objects.using(instance._state.db)
                                    .get_or_create(pk=instance.id, defaults={'name': instance.name}))
    except DatabaseError:
        log.warning('Unable to automatically create ampcms group post_save django_auth.group: %s' % instance)

def create_ampcms_site(sender, instance, created, **kwargs):
    try:
        if created:
            site, site_created = (AmpCmsSite.objects.using(instance._state.db)
                                  .get_or_create(pk=instance.id, defaults={'domain': instance.domain,
                                                                           'name': instance.name}))
    except DatabaseError:
        log.warning('Unable to automatically create ampcms site post_save django_auth.site: %s' % instance)

post_save.connect(create_ampcms_user, sender=DjangoUser)
post_save.connect(create_ampcms_group, sender=DjangoGroup)
post_save.connect(create_ampcms_site, sender=DjangoSite)
