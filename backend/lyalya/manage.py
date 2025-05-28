#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import argparse
import os
import sys


def main():
    """Run administrative tasks."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--settings', dest='settings', action='store', default=None)
    args, unknown = parser.parse_known_args()
    
    if args.settings is not None:
        os.environ['DJANGO_SETTINGS_MODULE'] = args.settings
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lyalya.settings')

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
