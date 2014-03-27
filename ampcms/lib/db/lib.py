from ampcms.conf import settings

def get_database_by_host(host):
    database = settings.AMPCMS_HOST_DATABASES.get(host)
    if database is not None and database in settings.DATABASES:
        return database
    else:
        return None