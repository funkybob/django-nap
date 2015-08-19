#!/usr/bin/env python

# Adapted from https://raw.githubusercontent.com/hzy/django-polarize/master/runtests.py

import sys

from django.conf import settings
from django.core.management import execute_from_command_line

import django

if django.VERSION < (1, 6):
    extra_settings = {
        'TEST_RUNNER': 'discover_runner.DiscoverRunner',
    }
else:
    extra_settings = {}


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=(
            'tests',
        ),
        MIDDLEWARE_CLASSES=[],
        ROOT_URLCONF='tests.urls',
        **extra_settings
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'tests']
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
