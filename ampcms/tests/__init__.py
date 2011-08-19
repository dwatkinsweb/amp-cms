import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Attempt to import settings to see if it is accessible
try:
    import settings
except:
    raise Exception('Unable to import settings. Make sure your settings file is accessible through from your python \
        path %s' % sys.path)
