#!/usr/bin/env python3
"""
Django Features Demo Script
===========================
Run this to see all Django features in action.

Usage:
    python3 manage.py shell < demo_script.py
    
Or in the shell:
    exec(open('demo_script.py').read())
"""

import os
import django

# Setup Django (only needed when running standalone script)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Student
from django.contrib.auth.models import User
from django.db.models import Count

print("=" * 60)
print("DJANGO FEATURES DEMONSTRATION")
print("=" * 60)

# ============================================================================
# PART 1: ORM - Create Sample Data
# ============================================================================
print("\n📝 PART 1: ORM - Creating Sample Data")
print("-" * 40)

# Clear existing data
Student.objects.all().delete()

# Create students
students_data = [
    {"name": "Alice Cohen", "email": "alice@iitc.org", "role": "student"},
    {"name": "Bob Levy", "email": "bob@iitc.org", "role": "teacher"},
    {"name": "Charlie Israel", "email": "charlie@iitc.org", "role": "student"},
    {"name": "Dana Peretz", "email": "dana@iitc.org", "role": "admin"},
    {"name": "Eli Yosef", "email": "eli@iitc.org", "role": "student"},
]

created = []
for data in students_data:
    s = Student.objects.create(**data)
    created.append(s)
    print(f"  Created: {s}")

print(f"\n✅ Created {len(created)} students")

# ============================================================================
# PART 2: ORM - Querying
# ============================================================================
print("\n🔍 PART 2: ORM - Querying Data")
print("-" * 40)

print(f"\nTotal students: {Student.objects.count()}")

print("\nStudents by role:")
role_stats = Student.objects.values("role").annotate(count=Count("id"))
for stat in role_stats:
    print(f"  {stat['role']}: {stat['count']}")

print("\nActive students:")
active = Student.objects.filter(is_active=True)
for s in active[:3]:
    print(f"  - {s.name} ({s.email})")

print("\nSearch by name (contains 'a'):")
results = Student.objects.filter(name__icontains="a")
for s in results:
    print(f"  - {s.name}")

# ============================================================================
# PART 3: ORM - Update & Delete
# ============================================================================
print("\n✏️ PART 3: ORM - Update & Delete")
print("-" * 40)

# Update
student = Student.objects.first()
old_name = student.name
student.name = f"{student.name} (Updated)"
student.save()
print(f"  Updated: {old_name} → {student.name}")

# Delete
to_delete = Student.objects.filter(name__icontains="eli").first()
if to_delete:
    print(f"  Deleting: {to_delete}")
    to_delete.delete()
    print(f"  Remaining count: {Student.objects.count()}")

# ============================================================================
# PART 4: Authentication System
# ============================================================================
print("\n🔐 PART 4: Authentication System")
print("-" * 40)

# Show existing users
users = User.objects.all()
print(f"\nUsers in system: {users.count()}")
for u in users:
    status = []
    if u.is_superuser:
        status.append("superuser")
    if u.is_staff:
        status.append("staff")
    if not status:
        status.append("regular")
    print(f"  - {u.username} ({', '.join(status)})")

# ============================================================================
# PART 5: Model Metadata
# ============================================================================
print("\n📊 PART 5: Model Metadata")
print("-" * 40)

print(f"\nModel: Student")
print(f"  Table name: {Student._meta.db_table}")
print(f"  Fields:")
for field in Student._meta.fields:
    print(f"    - {field.name}: {field.__class__.__name__}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 60)
print("DEMO COMPLETE")
print("=" * 60)
print("\nKey Django features demonstrated:")
print("  ✅ ORM - Create, Read, Update, Delete without SQL")
print("  ✅ ORM - Filtering, aggregation, querying")
print("  ✅ Built-in Authentication system")
print("  ✅ Model metadata and introspection")
print("\nNext steps:")
print("  - Visit http://localhost:8000/admin/ for the admin panel")
print("  - Try the API: http://localhost:8000/api/students/")
print("  - See LAB_Django_Features.md for hands-on exercises")
