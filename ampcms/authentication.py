from django.contrib.auth.backends import ModelBackend
from ampcms.models import Page, Site

class ACLBackend(ModelBackend):
    def get_group_permissions(self, user_obj):
        if not hasattr(user_obj, '_group_acl_cache'):
            acl = Page.objects.active_site_pages(Site.objects.get_current()).filter(group__user=user_obj).values_list('module__name', 'name').order_by()
            user_obj._group_acl_cache = set(["%s.%s" % (ct, name) for ct, name in acl])
        return user_obj._group_acl_cache
    
    def get_all_permissions(self, user_obj):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_acl_cache'):
            acl = Page.objects.active_site_pages(Site.objects.get_current()).filter(user=user_obj).order_by()
            user_obj._acl_cache = set([u"%s.%s" % (p.module.name, p.name) for p in acl])
            user_obj._acl_cache.update(self.get_group_permissions(user_obj))
        return user_obj._acl_cache