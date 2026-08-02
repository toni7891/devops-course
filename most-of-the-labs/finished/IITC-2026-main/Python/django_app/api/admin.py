"""
=============================================================================
DJANGO ADMIN — Automatic CRUD Interface
=============================================================================

WHAT IS THE DJANGO ADMIN?
One of Django's "killer features": by registering your models here,
Django automatically generates a full web-based CRUD interface.

HOW IT WORKS:
1. The `admin` app inspects the model's _meta (fields, relationships, choices)
2. It auto-generates list views, detail views, and forms for the model
3. Authentication is built-in — only superusers can access /admin/ by default

TO USE IT:
1. python manage.py migrate        (creates auth tables)
2. python manage.py createsuperuser
3. python manage.py runserver
4. Visit http://localhost:8000/admin/

This is extremely useful for:
- Internal tools and dashboards
- Content management systems
- Data inspection during development
- Customer support teams who need to edit data without touching code
=============================================================================
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Customizes how Student appears in the admin panel.
    Even without this class (just admin.site.register(Student)),
    Django would generate a working CRUD interface.
    """

    # Columns to show in the list view
    list_display = ("id", "name", "email", "role", "is_active", "created_at")

    # Add filter sidebar on the right
    list_filter = ("role", "is_active")

    # Enable search box (searches these fields with LIKE queries)
    search_fields = ("name", "email")

    # Make is_active editable directly in the list view (no need to open each record)
    list_editable = ("is_active",)

    # Sort by newest first
    ordering = ("-created_at",)

    # Read-only fields in the detail view
    readonly_fields = ("created_at", "updated_at")
