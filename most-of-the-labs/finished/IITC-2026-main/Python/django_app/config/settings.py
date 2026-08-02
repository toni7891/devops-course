"""
=============================================================================
DJANGO SETTINGS
=============================================================================

WHAT IS THIS FILE?
settings.py is the single source of truth for your entire Django project's
configuration. Django reads this at startup and configures every subsystem.

HOW DOES DJANGO USE THIS?
Django's startup sequence (called when the server starts):
1. manage.py sets DJANGO_SETTINGS_MODULE=config.settings
2. Django imports this module lazily via django.conf.LazySettings
3. The Apps Registry (django.apps.registry.Apps) reads INSTALLED_APPS,
   imports each app's AppConfig, and registers all models
4. Database connections are configured from DATABASES
5. Middleware classes are imported and ordered
6. URL patterns are loaded from ROOT_URLCONF

KEY CONCEPTS:
- INSTALLED_APPS: Django only knows about apps listed here. Each app can
  contribute models (DB tables), templates, static files, management
  commands, and admin registrations.
- MIDDLEWARE: A list of classes that wrap every request/response in layers
  (like an onion). Each middleware's process_request runs top-down,
  and process_response runs bottom-up.
- DATABASES: Django's ORM can talk to SQLite, PostgreSQL, MySQL, Oracle.
  The abstraction means you switch DBs by changing this dict.
=============================================================================
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY — never commit a real secret key to version control
SECRET_KEY = "django-insecure-educational-key-do-not-use-in-production-abc123"

# debug=True shows detailed error pages with full tracebacks in the browser.
# NEVER enable in production — it exposes internal code and settings.
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# ---------------------------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------------------------
# Django discovers all functionality through apps. This list controls:
#   - Which models get DB tables (via migrations)
#   - Which templates are found
#   - Which management commands are available
#   - What appears in the admin panel

INSTALLED_APPS = [
    # Django's own built-in apps (these are just Django apps too!)
    "django.contrib.admin",        # The /admin panel
    "django.contrib.auth",         # Authentication framework (User model, login)
    "django.contrib.contenttypes", # Generic relations between models
    "django.contrib.sessions",     # Server-side session storage
    "django.contrib.messages",     # One-time flash messages
    "django.contrib.staticfiles",  # Serving CSS/JS/images

    # Our custom app — defined in the api/ directory
    "api",
]


# ---------------------------------------------------------------------------
# MIDDLEWARE — The Onion Model
# ---------------------------------------------------------------------------
# Middleware is a list of classes that wrap every request/response.
# Think of it like a pipeline of decorators around your views.
#
# Request flow (TOP to BOTTOM through this list):
#   SecurityMiddleware → SessionMiddleware → ... → View
# Response flow (BOTTOM to TOP through this list):
#   View → ... → SessionMiddleware → SecurityMiddleware
#
# Each class implements process_request(request) and/or process_response(request, response)
#
# Example: SessionMiddleware reads a session cookie on the way IN,
#          loads session data into request.session, then on the way OUT
#          saves any changes back to the DB and sets the cookie.

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",      # HTTPS redirects, HSTS headers
    "django.contrib.sessions.middleware.SessionMiddleware",  # Session support
    "django.middleware.common.CommonMiddleware",           # URL normalization
    "django.middleware.csrf.CsrfViewMiddleware",           # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Attaches request.user
    "django.contrib.messages.middleware.MessageMiddleware",  # Flash messages
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
]


# ---------------------------------------------------------------------------
# URL CONFIGURATION
# ---------------------------------------------------------------------------
# Django starts URL resolution at this module. It imports `urlpatterns` and
# tries to match each pattern in order against the incoming request path.
ROOT_URLCONF = "config.urls"


# ---------------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,  # Look for templates in each app's templates/ folder
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ---------------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------------
# Django's ORM abstracts the database completely.
# Switching from SQLite to PostgreSQL = change 2 lines here.
# SQLite is fine for development and small apps.
# PostgreSQL is recommended for production.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# For PostgreSQL it would look like:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "mydb",
#         "USER": "myuser",
#         "PASSWORD": "mypassword",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }


# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True  # Store datetimes in UTC in the DB — always do this


# ---------------------------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------------------------
# In development, Django's staticfiles app serves files from each app's
# static/ folder. In production, run `collectstatic` and serve with nginx.
STATIC_URL = "static/"


# ---------------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------------------------
# Django 3.2+ default: BigAutoField (64-bit int) instead of AutoField (32-bit)
# This avoids overflow issues in large tables.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
