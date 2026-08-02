"""
=============================================================================
DJANGO MODELS — The ORM (Object-Relational Mapper)
=============================================================================

WHAT IS AN ORM?
An ORM lets you define database tables as Python classes and interact with
the database using Python instead of writing raw SQL.

HOW DJANGO'S ORM WORKS BEHIND THE SCENES:

1. MODEL DEFINITION → TABLE SCHEMA
   When you subclass django.db.models.Model, Django's metaclass
   (ModelBase) inspects all class attributes at import time, collects
   Field objects (CharField, IntegerField, etc.), and builds an internal
   Options object (_meta) that describes the table structure.

2. MIGRATIONS
   `python manage.py makemigrations` compares the current model definitions
   to the last known state (stored in migration files) and generates
   Python migration files describing what changed.
   `python manage.py migrate` runs those files and executes the SQL:
       CREATE TABLE api_student (
           id BIGINT PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(100) NOT NULL,
           ...
       );

3. QUERYSETS — LAZY EVALUATION
   Student.objects.all() does NOT hit the database immediately.
   It returns a QuerySet object — a description of a query.
   The SQL only executes when you iterate, slice, or call len().
   This allows Django to optimize: Student.objects.filter(role="admin")
   generates WHERE role='admin' in SQL, not Python-level filtering.

4. THE MANAGER
   Student.objects is an instance of Manager, which is the interface
   for database-level operations. You can write custom managers for
   common query patterns.

BENEFIT: Your Python code doesn't care if the DB is SQLite or PostgreSQL.
         The ORM generates the correct SQL dialect for each.
=============================================================================
"""

from django.db import models


class Student(models.Model):
    """
    Represents a student in the database.

    Django automatically adds an `id` field (BigAutoField primary key)
    because DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField" in settings.

    The table name is automatically: <app_label>_<model_name_lowercase>
    So this becomes: api_student
    """

    # CharField maps to VARCHAR in SQL.
    # max_length is required — Django validates this at the Python level.
    name = models.CharField(max_length=100)

    # TextField maps to TEXT (no length limit).
    email = models.EmailField(unique=True)  # unique=True → UNIQUE constraint in DB

    # choices restricts valid values. Django validates this at the form/serializer
    # level, but the DB only sees the string values (not display names).
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    # BooleanField maps to BOOLEAN (or TINYINT on older DBs).
    is_active = models.BooleanField(default=True)

    # DateTimeField with auto_now_add=True sets the value to NOW() on INSERT,
    # and never changes it again — perfect for created_at timestamps.
    created_at = models.DateTimeField(auto_now_add=True)

    # auto_now=True updates the value to NOW() on every save() call.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta inner class controls table-level options:
        - ordering: default sort order for querysets
        - db_table: override the auto-generated table name
        - indexes: add database indexes for query optimization
        - verbose_name: human-readable name shown in admin
        """
        ordering = ["-created_at"]  # Newest first (minus = descending)
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        """
        Django uses this in the admin panel and when printing objects.
        Always define __str__ on your models.
        """
        return f"{self.name} ({self.role})"

    # -------------------------------------------------------------------------
    # QuerySet Examples (what you'd use in views)
    # -------------------------------------------------------------------------
    # Student.objects.all()                     → SELECT * FROM api_student
    # Student.objects.filter(role="student")    → SELECT * WHERE role='student'
    # Student.objects.get(id=1)                 → SELECT * WHERE id=1 (raises if not found)
    # Student.objects.create(name="Alice", ...) → INSERT INTO ...
    # student.save()                            → INSERT or UPDATE
    # student.delete()                          → DELETE WHERE id=...
    # Student.objects.count()                   → SELECT COUNT(*) FROM ...
    # Student.objects.order_by("name")          → ORDER BY name ASC
