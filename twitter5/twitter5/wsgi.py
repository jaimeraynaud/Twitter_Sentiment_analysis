"""
WSGI config for twitter5 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter5.settings')

application = get_wsgi_application()
