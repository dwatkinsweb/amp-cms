from ampcms.conf import settings

def javascript_config(request):
    return {'AMPCMS_JAVASCRIPT_CONFIG': settings.AMPCMS_JAVASCRIPT_CONFIG}