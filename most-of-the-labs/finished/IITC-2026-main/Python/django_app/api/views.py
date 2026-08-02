"""
=============================================================================
DJANGO VIEWS — Request Handlers
=============================================================================

WHAT IS A VIEW?
In Django, a "view" is any callable that takes an HttpRequest and returns
an HttpResponse. It's the equivalent of a "controller" in MVC terminology.
Django's pattern is actually called MTV: Model-Template-View.

TWO STYLES OF VIEWS:

1. FUNCTION-BASED VIEWS (FBV) — simple functions
   - Easy to understand, explicit
   - Handle HTTP methods with if/elif
   - Good for simple or one-off endpoints

2. CLASS-BASED VIEWS (CBV) — classes with method dispatch
   - Django calls .get() for GET, .post() for POST, etc.
   - Built-in generic views: ListView, DetailView, CreateView eliminate boilerplate
   - Better for REST-style CRUD where you have many endpoints with similar logic

HOW THE REQUEST REACHES A VIEW:
Browser request → Middleware (top-down) → URL resolver → View function
View function → Middleware (bottom-up) → Browser response

The view has access to:
  request.method         → "GET", "POST", "PUT", "DELETE", etc.
  request.GET            → Query string parameters (MultiValueDict)
  request.POST           → Form data (MultiValueDict)
  request.body           → Raw request body bytes
  request.user           → The logged-in user (or AnonymousUser)
  request.session        → Server-side session dict
  request.META           → All HTTP headers + WSGI environ
=============================================================================
"""

import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Student

# UNCOMMENT FOR AUTH EXERCISE:
# from django.contrib.auth.decorators import login_required


# =============================================================================
# STYLE 1: FUNCTION-BASED VIEW
# =============================================================================

# UNCOMMENT FOR AUTH EXERCISE (add above @csrf_exempt):
# @login_required
@csrf_exempt  # For this educational API we disable CSRF. In production, use proper CSRF handling.
def student_list(request):
    """
    Function-based view handling GET and POST for /api/students/

    BEHIND THE SCENES:
    Django calls this function directly with the HttpRequest object.
    The @csrf_exempt decorator wraps this function, replacing it with
    a new function that sets request.csrf_processing_done = True,
    which tells CsrfViewMiddleware to skip the CSRF check.
    """
    if request.method == "GET":
        # QuerySet is lazy — no SQL yet
        queryset = Student.objects.all()

        # Optional filtering via query string: /api/students/?role=teacher
        role = request.GET.get("role")
        if role:
            # .filter() adds a WHERE clause to the SQL query
            queryset = queryset.filter(role=role)

        # SQL executes HERE when we iterate the queryset with list()
        # Generated SQL: SELECT id, name, email, role, is_active, created_at, updated_at
        #                FROM api_student [WHERE role='teacher']
        #                ORDER BY created_at DESC
        students = list(queryset.values("id", "name", "email", "role", "is_active"))

        # JsonResponse serializes the list to JSON and sets Content-Type: application/json
        return JsonResponse(students, safe=False)  # safe=False allows lists (not just dicts)

    elif request.method == "POST":
        try:
            # request.body is raw bytes — we must decode JSON manually
            # (Django doesn't have built-in JSON body parsing like Flask/FastAPI)
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        # Validate required fields
        if not data.get("name") or not data.get("email"):
            return JsonResponse({"error": "name and email are required"}, status=400)

        # Model.objects.create() = instantiate + validate + INSERT in one call
        # Django runs field-level validators before saving
        try:
            student = Student.objects.create(
                name=data["name"],
                email=data["email"],
                role=data.get("role", "student"),
            )
        except Exception as e:
            # email has unique=True — IntegrityError if duplicate
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "role": student.role,
            "created_at": student.created_at.isoformat(),
        }, status=201)

    # Django returns 405 if we return None for unhandled methods,
    # but it's better to be explicit:
    return JsonResponse({"error": "Method not allowed"}, status=405)


# =============================================================================
# STYLE 2: CLASS-BASED VIEW
# =============================================================================

@method_decorator(csrf_exempt, name="dispatch")
class StudentDetailView(View):
    """
    Class-based view handling GET, PUT, DELETE for /api/students/<id>/

    BEHIND THE SCENES:
    Django calls StudentDetailView.as_view() in urls.py.
    as_view() returns a function (closure) that:
      1. Creates a new instance of StudentDetailView for each request
      2. Sets instance attributes from URL kwargs (self.kwargs, self.args)
      3. Calls self.dispatch(request, *args, **kwargs)
      4. dispatch() looks at request.method.lower() and calls the matching method

    The @method_decorator applies @csrf_exempt to the dispatch() method.
    """

    def get_object(self, student_id):
        """
        Helper to fetch a student or return None.
        In a real app, use Django's get_object_or_404() shortcut.
        """
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return None

    def get(self, request, student_id):
        """GET /api/students/<student_id>/ — Retrieve one student"""
        student = self.get_object(student_id)
        if not student:
            return JsonResponse({"error": "Student not found"}, status=404)

        return JsonResponse({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "role": student.role,
            "is_active": student.is_active,
            "created_at": student.created_at.isoformat(),
            "updated_at": student.updated_at.isoformat(),
        })

    def put(self, request, student_id):
        """PUT /api/students/<student_id>/ — Update a student"""
        student = self.get_object(student_id)
        if not student:
            return JsonResponse({"error": "Student not found"}, status=404)

        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        # Only update fields that were provided in the request
        if "name" in data:
            student.name = data["name"]
        if "role" in data:
            student.role = data["role"]
        if "is_active" in data:
            student.is_active = data["is_active"]

        # save() with update_fields generates: UPDATE api_student SET ... WHERE id=...
        # Without update_fields, Django generates UPDATE with ALL fields (wasteful)
        student.save()

        return JsonResponse({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "role": student.role,
            "updated_at": student.updated_at.isoformat(),
        })

    def delete(self, request, student_id):
        """DELETE /api/students/<student_id>/ — Delete a student"""
        student = self.get_object(student_id)
        if not student:
            return JsonResponse({"error": "Student not found"}, status=404)

        student.delete()
        # 204 No Content — success with no response body
        return HttpResponse(status=204)


# =============================================================================
# EXAMPLE: Showing Django's Admin and ORM power
# =============================================================================

def stats_view(request):
    """
    GET /api/stats/ — Demonstrate aggregation queries

    Django's ORM can do complex SQL through the queryset API.
    These calls generate efficient SQL, not Python loops.
    """
    from django.db.models import Count

    stats = {
        "total_students": Student.objects.count(),
        # .aggregate() → SELECT COUNT(*) GROUP BY role
        "by_role": list(
            Student.objects
            .values("role")
            .annotate(count=Count("id"))
        ),
        "active_count": Student.objects.filter(is_active=True).count(),
    }

    return JsonResponse(stats)
