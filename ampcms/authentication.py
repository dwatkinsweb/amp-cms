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
from ampcms.utils import get_current_request
from ampcms import const as C

class ACLBackend(ModelBackend):
    def get_group_permissions(self, user):
        if not hasattr(user, C.GROUP_ACL_CACHE):
            site = Site.objects.get_by_request(get_current_request())
            acl = Page.objects.filter(module__site=site).filter(user=user).values_list('module__name', 'name').order_by()
            setattr(user, C.GROUP_ACL_CACHE, set(["%s.%s" % (ct, name) for ct, name in acl]))
        return getattr(user, C.GROUP_ACL_CACHE)
    
    def get_all_permissions(self, user):
        if user.is_anonymous():
            return set()
        if not hasattr(user, C.GROUP_ACL_CACHE):
            site = Site.objects.get_by_request(get_current_request())
            acl = Page.objects.filter(module__site=site).filter(group__user=user).values_list('module__name', 'name').order_by()
            acl_cache = set(["%s.%s" % (ct, name) for ct, name in acl])
            acl_cache.update(self.get_group_permissions(user))
            setattr(user, C.GROUP_ACL_CACHE, acl_cache)
        return getattr(user, C.GROUP_ACL_CACHE)
