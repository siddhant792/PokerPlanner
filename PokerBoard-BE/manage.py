#!/usr/bin/env python
import os
import sys
import class_settings


def set_settings():
    """
    Set local/production settings according to usage
    """
    if(os.path.exists("poker/settings/local.py")):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker.settings.base")
    os.environ.setdefault('DJANGO_SETTINGS_CLASS', 'Setting')
    class_settings.setup()


if __name__ == "__main__":
    set_settings()
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
