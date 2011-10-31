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

from django.http import Http404
from ampcms.models import User, Group

import logging
log = logging.getLogger(__name__)

class UserManagement:
    ''' This is used to replace the default request.user object with our extended user object '''
    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                request.user = User.objects.get(pk=request.user.id)
            except User.DoesNotExist:
                log.exception('Error replacing user %s with custom user object' % request.user)
                raise Http404
            # TODO: Find a way to replace this with an actual manager instead of a queryset
            request.user.groups = Group.objects.filter(pk__in=[group.id for group in request.user.groups.all()])
