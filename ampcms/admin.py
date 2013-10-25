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

try:
    from import_export.admin import ImportExportModelAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm, UserCreationForm as DjangoUserCreationForm
from django.contrib.sites.admin import SiteAdmin as DjangoSiteAdmin
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ampcms.models import Module, Page, Pagelet, PageletAttribute, User, Group, AmpCmsSite, PageDetails, PageletDetails, ModuleDetails
from ampcms.conf import settings

class SiteAdmin(DjangoSiteAdmin):
    list_display = ('domain', 'name', 'skin', 'private')
    list_filter = ('private',)

class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User

class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User

class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None,
            {'fields': ('username', 'password')}),
        (_('Personal Info'),
            {'fields': ('first_name', 'last_name', 'email')}),
        (_('Page Permissions'),
            {'classes': ('collapse',),
             'fields': ('acl_pages', 'acl_pagelets')}),
        (_('Other Permissions'),
            {'classes': ('collapse',),
             'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important Dates'),
            {'classes': ('collapse',),
             'fields': ('last_login', 'date_joined')}),
        (_('Groups'),
            {'fields': ('groups',)}),
    )
    filter_horizontal = ('user_permissions', 'acl_pages', 'acl_pagelets', 'groups')
    form = UserChangeForm
    add_form = UserCreationForm

class GroupAdmin(DjangoGroupAdmin):
    filter_horizontal = ('permissions', 'acl_pages', 'acl_pagelets')

class ModuleDetailsInline(admin.TabularInline):
    model = ModuleDetails
    extra = 0

class PageDetailsInline(admin.TabularInline):
    model = PageDetails
    extra = 0

class PageletDetailsInline(admin.TabularInline):
    model = PageletDetails
    extra = 0

class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    readonly_fields = ['admin_link']
 
class PageletInline(admin.TabularInline):
    model = Pagelet
    extra = 0
    readonly_fields = ['admin_link']
    exclude = ['classes']

class PageletAttributeInline(admin.TabularInline):
    model = PageletAttribute

class ModuleForm(forms.ModelForm):
    model = Module

class ModuleAdmin(ModelAdmin):
    fieldsets = (
        ('Names', {'fields': ('name', 'icon')}),
        ('Other', {'fields': ('site', 'order', 'active', 'show_in_navigation')}),
        ('Redirects', {'classes': ('collapse',),
                       'fields': ('redirect_module', 'redirect_url')}))
    list_display = ('name', 'title', 'active', 'order', 'site', 'view_on_site')
    list_filter = ('active', 'site')
    list_editable = ('order',)
    inlines = [ModuleDetailsInline, PageInline]
    actions = ['activate', 'deactivate']
    ordering = ['site__domain', 'name']
    
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js',)
        css = {
            'all': ('ampcms/css/admin-extended.css',)
        }
    
    def activate(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            msg = '1 module was activated'
        else:
            msg = '%s modules were activated' % rows_updated
        self.message_user(request, msg)
    activate.short_description = 'Activate selected modules'
    
    def deactivate(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            msg = '1 module was activated'
        else:
            msg = '%s modules were activated' % rows_updated
        self.message_user(request, msg)
    deactivate.short_description = 'Deactivate selected modules'
    
    def view_on_site(self, obj):
        if obj.active:
            return '<a href="http://%s/%s">View on Site</a>' % (obj.site, obj.name)
        else:
            return ''
    view_on_site.allow_tags = True

class PageAdmin(ModelAdmin):
    fieldsets = (
        ('Names', {'fields': ('name', 'icon')}),
        ('Objects', {'fields': ('module', 'page_class',)}),
        ('Other', {'fields': ('order', 'private', 'active', 'show_in_navigation')}))
    list_display = ('full_name', 'name', 'title', 'site', 'module', 'page_class', 'active', 'order', 'view_on_site')
    list_filter = ('active', 'module__site', 'module', 'page_class')
    list_editable = ('order',)
    inlines = [PageDetailsInline, PageletInline]
    actions = ['activate', 'deactivate']
    ordering = ['module__site__domain', 'module__name', 'name']
    
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js',)
        css = {
            'all': ('ampcms/css/admin-extended.css',)
        }
    
    def site(self, obj):
        return obj.module.site
    site.short_description = 'Site'
    
    def activate(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            msg = '1 page was activated'
        else:
            msg = '%s pages were activated' % rows_updated
        self.message_user(request, msg)
    activate.short_description = 'Activate selected pages'
    
    def deactivate(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            msg = '1 page was activated'
        else:
            msg = '%s pages were activated' % rows_updated
        self.message_user(request, msg)
    deactivate.short_description = 'Deactivate selected pages'
    
    def full_name(self, obj):
        return '%s.%s' % (obj.module.name, obj.name)
    full_name.short_description = 'Page'
    
    def view_on_site(self, obj):
        if obj.active:
            return '<a href="http://%s/%s/%s">View on Site</a>' % (obj.module.site, obj.module.name, obj.name)
        else:
            return ''
    view_on_site.allow_tags = True

class PageletAdmin(ModelAdmin):
    fieldsets = (
        ('Names', {'fields': ('name',)}),
        ('Objects', {'fields': ('page', 'pagelet_class', 'application', 'starting_url', 'classes')}),
        ('Other', {'fields': ('order', 'active')}))
    list_display = ('full_name', 'name', 'title', 'page', 'active', 'pagelet_class', 'order')
    list_filter = ('active', 'page__module__site', 'page__module', 'page', 'pagelet_class')
    inlines = [PageletDetailsInline, PageletAttributeInline]
    actions = ['activate', 'deactivate']
    ordering = ['page__module__site__domain', 'page__module__name', 'page__name', 'name']
    
    class Media:
        css = {
            'all': ('ampcms/css/admin-extended.css',)
        }
    
    def full_name(self, obj):
        return '%s.%s.%s' % (obj.page.module.name, obj.page.name, obj.name)
    full_name.short_description = 'Pagelet'
    
    def activate(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            msg = '1 pagelet was activated'
        else:
            msg = '%s pagelets were activated' % rows_updated
        self.message_user(request, msg)
    activate.short_description = 'Activate selected pagelets'
    
    def deactivate(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            msg = '1 pagelet was activated'
        else:
            msg = '%s pagelets were activated' % rows_updated
        self.message_user(request, msg)
    deactivate.short_description = 'Deactivate selected pagelets'

if settings.AMPCMS_WYSIWYG == 'ckeditor':
    from ckeditor.widgets import CKEditorWidget
    class PageletAdminForm(forms.ModelForm):
        content = forms.CharField(widget=CKEditorWidget(), required=False)
        class Meta:
            model = Pagelet
    PageletAdmin.form = PageletAdminForm

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(AmpCmsSite, SiteAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Pagelet, PageletAdmin)