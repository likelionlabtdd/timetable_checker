"""
WSGI config for timetable_checker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/opt/python/current/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetable_checker.settings')

application = get_wsgi_application()
