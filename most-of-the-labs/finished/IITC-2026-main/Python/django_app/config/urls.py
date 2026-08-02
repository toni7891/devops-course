"""
=============================================================================
ROOT URL CONFIGURATION
=============================================================================

WHAT IS THIS?
This is the top-level URL router for the entire Django project.
Django reads this module first when resolving any incoming URL.

HOW DOES URL RESOLUTION WORK?
1. A request arrives at /api/users/
2. Django loads `urlpatterns` from this file (ROOT_URLCONF in settings)
3. Django tries each pattern in order using re.fullmatch() internally
4. `include("api.urls")` means: strip the matched prefix ("/api/") and
   pass the rest ("/users/") to the api app's own urlpatterns
5. The api app's urls.py then matches "/users/" and calls the view

This two-level URL structure is Django's way of keeping each app
self-contained. Each app owns its own URL patterns, which are
"included" at a prefix defined here.

WHY IS THIS BETTER THAN ONE BIG URL FILE?
- Apps become reusable: mount `api` at /api/ in one project, /v1/ in another
- Each app team owns their own urls.py
- Easier to read and maintain
=============================================================================
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin panel — try /admin/ after creating a superuser
    # `admin.site.urls` is itself a URL conf returned by the admin app
    path("admin/", admin.site.urls),

    # Built-in login/logout views (required for @login_required decorator)
    # These provide the /accounts/login/ and /accounts/logout/ URLs
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Mount our api app's URL patterns under the /api/ prefix.
    # include() imports api.urls and prefixes all its patterns with "api/"
    path("api/", include("api.urls")),
]
