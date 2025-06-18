#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import argparse
import os
import sys
import psycopg2
import time
from django.conf import settings

def wait_for_db(max_attempts=70):
    db_config = {
        'dbname': settings.DATABASES['default']['NAME'],
        'user': settings.DATABASES['default']['USER'],
        'password': settings.DATABASES['default']['PASSWORD'],
        'host': settings.DATABASES['default']['HOST'],
        'port': settings.DATABASES['default'].get('PORT', '5432'),
    }
    attempts = 0
    while True:
        conn = None
        try:
            conn = psycopg2.connect(dbname=db_config['dbname'], user=db_config['user'], password=db_config['password'], host=db_config['host'], port=db_config['port'])
            conn.close()
        except Exception as e:
            attempts += 1
            print(f"Not connect to PostgreSQL. att: {attempts}/{max_attempts}")
            time.sleep(5)
        if attempts >= max_attempts:
            print(f"The maximum number of attempts to connect to the database has been reached. att: {attempts}/{max_attempts}")
            break

def main():
    """Run administrative tasks."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--settings', dest='settings', action='store', default=None)
    parser.add_argument('--waitpg', dest='waitpg', action='store', default=None)
    args, unknown = parser.parse_known_args()
    
    if args.settings is not None:
        os.environ['DJANGO_SETTINGS_MODULE'] = args.settings
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyalya.settings')

    if args.waitpg is not None:
        wait_for_db()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
