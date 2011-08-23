from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm, UserCreationForm as DjangoUserCreationForm
from django.contrib.sites.admin import SiteAdmin as DjangoSiteAdmin
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from ampcms.models import Module, Page, Pagelet, PageletAttribute, User, Group, Site
from ampcms.conf import settings

class SiteAdmin(DjangoSiteAdmin):
    list_display = ('domain', 'name', 'private')

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

class PageInline(admin.TabularInline):
    model = Page
    extra = 0
 
class PageletInline(admin.TabularInline):
    model = Pagelet
    extra = 0

class PageletAttributeInline(admin.TabularInline):
    model = PageletAttribute

class ModuleForm(forms.ModelForm):
    model = Module

class ModuleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Names', {'fields': ('name', 'title')}),
        ('Other', {'fields': ('site', 'active',)}))
    list_display = ('name', 'title', 'active', 'order', 'site', 'view_on_site')
    list_filter = ('active','site')
    list_editable = ('order',)
    inlines = [PageInline]
    actions = ['activate', 'deactivate']
    
    class Media:
        js = (
            'ampcms/js/jquery.min.js',
            'ampcms/js/jquery-ui.min.js',
            'ampcms/js/jquery.sortable-result_list.js',
            'ampcms/js/sortable-result_list.js',
            'ampcms/js/jquery.sortable-inline.js',
            'ampcms/js/sortable-inline.js',)
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

class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Names', {'fields': ('name', 'title')}),
        ('Objects', {'fields': ('module', 'page_class', 'application', 'pagelet_layout')}),
        ('Other', {'fields': ('order', 'active')}))
    list_display = ('full_name', 'name', 'title', 'module', 'page_class', 'active', 'order', 'view_on_site')
    list_filter = ('active', 'module', 'page_class')
    inlines = [PageletInline]
    actions = ['activate', 'deactivate']
    
    class Media:
        js = (
            'ampcms/js/jquery.min.js',
            'ampcms/js/jquery-ui.min.js',
            'ampcms/js/jquery.sortable-inline.js',
            'ampcms/js/sortable-inline.js',)
        css = {
            'all': ('ampcms/css/admin-extended.css',)
        }
    
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

class PageletAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Names', {'fields': ('name', 'title')}),
        ('Objects', {'fields': ('page', 'pagelet_class', 'application', 'starting_url', 'js_files', 'css_files', 'classes', 'content')}),
        ('Other', {'fields': ('order', 'active')}))
    list_display = ('full_name', 'name', 'title', 'page', 'active', 'pagelet_class', 'order')
    list_filter = ('active', 'page', 'pagelet_class')
    inlines = [PageletAttributeInline]
    actions = ['activate', 'deactivate']
    
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
        content = forms.CharField(widget=CKEditorWidget())
        class Meta:
            model = Pagelet
        class Media:
            js = ('/media/ckeditor/ckeditor/ckeditor.js',)
    PageletAdmin.form = PageletAdminForm

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Pagelet, PageletAdmin)
