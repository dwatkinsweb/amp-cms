import re
from ampcms.conf import settings
from ampcms.models import AmpCmsSite
from django.contrib.staticfiles import finders

JS_PREFIX_RE = re.compile(r'^(/?)((js/)?)(.*)')

def javascript_config(request):
    site = AmpCmsSite.objects.get_by_request(request)
    skin = site.skin
    if skin:
        config = JS_PREFIX_RE.sub(r'\1\2%s/\4' % skin, settings.AMPCMS_JAVASCRIPT_CONFIG)
        found = finders.find(config)
        if not found:
            config = settings.AMPCMS_JAVASCRIPT_CONFIG
    return {'AMPCMS_JAVASCRIPT_CONFIG': config}