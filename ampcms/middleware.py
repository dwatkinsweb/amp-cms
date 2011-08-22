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