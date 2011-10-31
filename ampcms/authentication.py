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
