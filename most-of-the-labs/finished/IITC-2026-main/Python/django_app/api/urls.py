"""
=============================================================================
APP-LEVEL URL CONFIGURATION
=============================================================================

HOW URL RESOLUTION WORKS IN DJANGO:
1. config/urls.py matches "api/" and calls include("api.urls")
2. Django strips "api/" from the path and tries to match the remainder
   against THIS urlpatterns list
3. The first matching pattern wins — order matters!

URL PATTERN SYNTAX:
- path("students/", view)      → matches exactly "/api/students/"
- path("students/<int:id>/", view) → matches "/api/students/42/"
  The <int:id> part is a "path converter":
    int  → digits only, converted to Python int
    str  → any non-slash string (default)
    slug → letters, numbers, hyphens, underscores
    uuid → UUID format
    path → any string including slashes

TRAILING SLASHES:
Django's CommonMiddleware appends a trailing slash if APPEND_SLASH=True
(the default) and the URL without slash doesn't match but with slash does.
That's why Django URLs conventionally end with "/".
=============================================================================
"""

from django.urls import path
from . import views

# `app_name` enables URL namespacing:
# In templates: {% url 'api:student_list' %}
# In Python:    reverse('api:student_list')
# This prevents name collisions when multiple apps have a view named "student_list"
app_name = "api"

urlpatterns = [
    # /api/students/ → function-based view (handles GET and POST)
    path("students/", views.student_list, name="student_list"),

    # /api/students/42/ → class-based view (handles GET, PUT, DELETE)
    # .as_view() converts the class into a callable view function
    path("students/<int:student_id>/", views.StudentDetailView.as_view(), name="student_detail"),

    # /api/stats/
    path("stats/", views.stats_view, name="stats"),
]
