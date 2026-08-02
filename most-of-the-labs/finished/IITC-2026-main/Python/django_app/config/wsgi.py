"""
=============================================================================
WSGI CONFIGURATION
=============================================================================

WHAT IS WSGI?
WSGI (Web Server Gateway Interface, PEP 3333) is the standard interface
between Python web applications and web servers.

HOW IT WORKS:
1. A production web server (nginx) receives the HTTP request from the browser
2. nginx passes it to a WSGI server (Gunicorn, uWSGI) via a socket
3. The WSGI server calls your application like this:
       response = application(environ, start_response)
   where `environ` is a dict of HTTP headers, path, query string, etc.
4. `application` here is the Django WSGI app — it processes the request
   through middleware → URL routing → view → middleware → response
5. The WSGI server sends the response bytes back to nginx → browser

PRODUCTION DEPLOYMENT:
    gunicorn config.wsgi:application --workers 4 --bind 0.0.0.0:8000

Note: For async support, use ASGI (asgi.py) with uvicorn instead.
=============================================================================
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# This callable IS your Django application.
# Gunicorn will import this and call it for every request.
application = get_wsgi_application()
