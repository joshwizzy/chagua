"""
WSGI config for CHAGUA E-Commerce Platform.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chagua_backend.settings')

application = get_wsgi_application()
