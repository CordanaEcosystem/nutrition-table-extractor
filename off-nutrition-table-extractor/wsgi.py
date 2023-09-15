"""
WSGI config for nutritionextraction_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# this module name was changed to make it work
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "off-nutrition-table-extractor.settings")

application = get_wsgi_application()
