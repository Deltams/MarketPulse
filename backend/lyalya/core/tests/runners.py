from django.conf import settings

def get_db_test():
    return list(settings.DATABASES.keys() - {'default'})