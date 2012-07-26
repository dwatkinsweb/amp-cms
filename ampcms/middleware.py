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

from ampcms.models import User
from ampcms.utils import set_current_request

import logging
log = logging.getLogger(__name__)

class UserManagement:
    ''' This is used to replace the default request.user object with our extended user object '''
    def process_request(self, request):
        if request.user.is_authenticated():
            request.user, created = User.objects.get_or_create(pk=request.user.pk,
                                                               defaults={'username':request.user.username,
                                                                         'first_name':request.user.first_name,
                                                                         'last_name':request.user.last_name,
                                                                         'email':request.user.email,
                                                                         'password':request.user.password,
                                                                         'is_staff':request.user.is_staff,
                                                                         'is_active':request.user.is_active,
                                                                         'is_superuser':request.user.is_superuser,
                                                                         'last_login':request.user.last_login,
                                                                         'date_joined':request.user.date_joined})

class RequestThreadStorage:
    def process_request(self, request):
        set_current_request(request)
