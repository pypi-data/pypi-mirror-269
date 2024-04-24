#!/usr/bin/env python

import os
import sys

import django
from django.conf import settings

if "test" in sys.argv:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basxconnect.core.tests.settings")
else:
    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "basxbread",
        "djmoney",
        "basxconnect.core",
        "basxconnect.contributions",
        "basxconnect.mailer_integration",
        "basxconnect.invoicing",
        "basxconnect.projects",
    ]
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        USE_I18N=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        MIDDLEWARE_CLASSES=(),
        SITE_ID=1,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_URL="static/",
    )
    django.setup()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
