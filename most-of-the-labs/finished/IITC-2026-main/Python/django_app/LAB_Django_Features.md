# Django Lab: From Flask to Django - A Beginner's Journey

> **You know Flask. Now let's meet Django.**
>
> In Flask, you write everything yourself. In Django, many things come "batteries included".
> This lab will show you exactly what that means.

---

## The Story: The Restaurant Manager

Imagine you run a restaurant:

**Flask is like running a food truck:**
- You decide everything: menu, layout, cash register, everything
- You build it all from scratch
- Freedom! But also... lots of work

**Django is like running a franchise restaurant:**
- The kitchen, tables, and cash register are already built
- You just customize for your needs
- Less freedom in some places, but you open for business **much faster**

---

## Chapter 1: The Database Problem (What is ORM?)

### The Problem You Face

In Flask, if you want to save a student to a database, you write SQL:

```python
# Flask style (what you know)
import sqlite3
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Insert a student
cursor.execute(
    "INSERT INTO students (name, email, role) VALUES (?, ?, ?)",
    ("Alice", "alice@school.com", "student")
)
conn.commit()

# Query all students
cursor.execute("SELECT * FROM students WHERE role = ?", ("student",))
students = cursor.fetchall()
```

**This works, but:**
- You write SQL by hand
- You manage database connections
- If you switch from SQLite to PostgreSQL, you rewrite queries
- It's repetitive and error-prone

### The Django Solution: ORM

**ORM = Object-Relational Mapping**

Think of it like a **translator** between Python and your database:

```
Your Python Code          The ORM (Translator)          The Database
     |                           |                            |
     |  Student.objects.all()      |     "SELECT * FROM student"  |
     |-------------------------->|----------------------------->|
     |                           |                            |
     |  [Student, Student...]    |     "Here are the rows"      |
     |<--------------------------|<-----------------------------|
```

Instead of writing SQL, you write Python:

```python
# Django style (what you'll learn)
from api.models import Student

# Insert a student - no SQL!
student = Student.objects.create(
    name="Alice",
    email="alice@school.com",
    role="student"
)

# Query all students - no SQL!
students = Student.objects.filter(role="student")
```

**The magic:** You never write SQL. Django translates your Python into SQL automatically.

---

## Setup (Do This First)

### Python Version

**This lab requires Python 3.14**

Check your version:
```bash
python3 --version
# Should show: Python 3.14.x
```

If you have a different version, install Python 3.14 from python.org

### Windows Users

**Option 1: Use Git Bash (Recommended)**
- Git Bash provides the same commands as macOS/Linux
- All commands below work exactly as written

**Option 2: Use Command Prompt/PowerShell**
Replace `python3` with `python` and `source venv/bin/activate` with `venv\Scripts\activate`:
```cmd
cd Python\django_app
python -m venv venv
venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Setup Commands (macOS/Linux/Git Bash)

Open your terminal and run these commands **in order**:

```bash
# 1. Navigate to the Django project
cd Python/django_app

# 2. Create virtual environment (first time only)
python3 -m venv venv

# 3. Activate your virtual environment
source venv/bin/activate

# 4. Create migration files (tells Django what tables to create)
python3 manage.py makemigrations

# 5. Apply migrations (actually creates the database tables)
python3 manage.py migrate

# 6. Create an admin user (for logging into /admin)
python3 manage.py createsuperuser
# Enter username, email, and password when prompted

# 7. Start the server
python3 manage.py runserver
```

**What are these commands doing?**

| Command | What it does | Why we need it |
|---------|--------------|----------------|
| `makemigrations` | Reads your `models.py` and creates migration files | Tells Django: "I need a table for Student" |
| `migrate` | Runs the migration files and creates actual database tables | Actually creates the `api_student` table in SQLite |
| `createsuperuser` | Creates an admin account | Lets you login to the admin panel |
| `runserver` | Starts the web server | Lets you visit http://localhost:8000 |

**Important:** You must run `makemigrations` AND `migrate` before using the ORM. Otherwise you'll get `no such table` errors.

**What is `runserver` doing?**

Django includes a built-in web server for development. In production, you'd use a proper WSGI server like Gunicorn.

**What's WSGI?** (Web Server Gateway Interface)
- It's the "language" between Python web apps and web servers
- Think of it as a **waiter** at a restaurant:
  - Takes orders from customers (HTTP requests)
  - Brings them to the kitchen (your Django code)
  - Delivers the food back (HTTP response)
- WSGI handles **one customer at a time** per worker (sync)
- For high traffic, you run multiple workers (like having multiple waiters)

---

## Chapter 2: Your First ORM Experience

### The Task: Manage Students Like a Pro

Let's see the ORM in action. Open a **new terminal** (keep the server running in the first one):

```bash
cd Python/django_app
source venv/bin/activate
python3 manage.py shell
```

You're now in Django's interactive shell. Type this line by line:

```python
from api.models import Student

# STEP 1: CREATE - Add students to the database
student1 = Student.objects.create(
    name="Alice Cohen",
    email="alice@iitc.org",
    role="student"
)
print(f"Created: {student1.name}")

student2 = Student.objects.create(
    name="Bob Levy",
    email="bob@iitc.org",
    role="teacher"
)
print(f"Created: {student2.name}")
```

**What just happened?**
- You created Python objects
- Django **automatically** saved them to the database
- You didn't write a single line of SQL

### Reading Data

```python
# STEP 2: READ - Get all students
all_students = Student.objects.all()
print("All students:", [f"{s.name} ({s.role})" for s in all_students])

# Filter: Only students (not teachers)
only_students = Student.objects.filter(role="student")
print("Only students:", [s.name for s in only_students])

# Get one specific student
alice = Student.objects.get(name="Alice Cohen")
print(f"Found: {alice.name}, email: {alice.email}")

# Count how many we have
print(f"Total students: {Student.objects.count()}")
```

**Compare to Flask:**

| Task | Flask (SQL) | Django (ORM) |
|------|-------------|--------------|
| Get all | `cursor.execute("SELECT * FROM students")` | `Student.objects.all()` |
| Filter | `cursor.execute("SELECT * WHERE role=?", ("student",))` | `Student.objects.filter(role="student")` |
| Count | `cursor.execute("SELECT COUNT(*) FROM students")` | `Student.objects.count()` |

### Updating and Deleting

```python
# STEP 3: UPDATE - Change Alice's role
alice = Student.objects.get(name="Alice Cohen")
alice.role = "teacher"
alice.save()
print(f"Updated {alice.name} to role: {alice.role}")

# STEP 4: DELETE - Remove Bob
bob = Student.objects.get(name="Bob Levy")
bob.delete()
print(f"Deleted Bob. Remaining: {Student.objects.count()}")
```

**The Pattern:**
1. **Create:** `Model.objects.create(field=value)`
2. **Read:** `Model.objects.all()`, `.filter()`, `.get()`
3. **Update:** Change object → `.save()`
4. **Delete:** `.delete()`

This is **CRUD** - Create, Read, Update, Delete - the four basic operations.

---

## Chapter 3: The Magic Admin Panel

Here's where Django really shines compared to Flask.

### The Scenario

Your boss says: *"I need to see all students, edit their info, and add new ones. Build me an admin dashboard."*

**In Flask:** You'd spend hours building HTML forms, handling POST requests, validation, etc.

**In Django:** It's already built. You just need to login.

### Try It Now

1. Make sure your server is running (`python3 manage.py runserver`)
2. Open your browser: http://localhost:8000/admin/
3. Login with the superuser you created
4. Click on "Students" under "API"

**What you see:**
- A list of all students with columns
- A search box to find students
- Filters on the right (by role, by active status)
- Buttons to add, edit, or delete

This entire interface was created **automatically** from your `Student` model. You wrote zero HTML, zero JavaScript.

### Admin Exercise

Try these actions:

1. **Add a student:** Click "Add Student" → Fill the form → Save
2. **Edit a student:** Click any name → Change something → Save
3. **Search:** Use the search box to find "Alice"
4. **Filter:** Click "Teacher" in the right sidebar
5. **Bulk actions:** Select multiple students → Choose "Delete" from dropdown

**Where is this configured?**

Look at `api/admin.py`:

```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("name", "email")
```

This simple code creates that entire admin interface!

---

## Chapter 4: Understanding the Architecture

### How Django is Organized

Think of a Django project like a company:

```
Your Django Project (the company)
│
├── config/              ← Company headquarters (settings, main routing)
│   ├── settings.py      ← "The rulebook" - database, installed apps, etc.
│   └── urls.py          ← "Reception" - where requests first arrive
│
└── api/                 ← A department (one app)
    ├── models.py        ← "Data department" - defines database tables
    ├── views.py         ← "Service department" - handles requests
    ├── urls.py          ← "Department routing" - app-specific URLs
    └── admin.py         ← "Management interface" - admin panel config
```

### The Request Journey

When you visit `http://localhost:8000/api/students/`:

```
1. Browser asks for /api/students/
         ↓
2. config/urls.py sees "api/" → sends to api/urls.py
         ↓
3. api/urls.py sees "students/" → calls student_list view
         ↓
4. views.py's student_list function runs
         ↓
5. Function queries database via models.py
         ↓
6. Returns JSON response to browser
```

### Compare to Flask

| | Flask | Django |
|---|-------|--------|
| **Entry point** | `app.py` | `manage.py` |
| **Routes** | `@app.route()` in same file | `urls.py` files |
| **Database** | You choose (SQLAlchemy, raw SQL) | Built-in ORM |
| **Admin** | Build yourself | Comes built-in |
| **Structure** | You decide | Django enforces conventions |

---

## Chapter 5: The Built-in Auth System

Django comes with a complete user authentication system. No need to build login/logout yourself.

### Explore Users

In the Django shell (`python3 manage.py shell`):

```python
from django.contrib.auth.models import User

# See all users
users = User.objects.all()
print([(u.username, u.email, "superuser" if u.is_superuser else "staff" if u.is_staff else "regular") for u in users])
```

**User Types:**
- **Regular user:** Can login to your site (if you allow)
- **Staff (`is_staff=True`):** Can access the admin panel
- **Superuser (`is_superuser=True`):** Can do everything in admin

You created a superuser when you ran `createsuperuser`.

### Create Users

```python
# Create a normal user
normal_user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='testpass123'
)

# Create a staff user (can access admin)
staff_user = User.objects.create_user(
    username='staff_member',
    email='staff@example.com',
    password='testpass123'
)
staff_user.is_staff = True
staff_user.save()
```

---

### Using Authentication in Your Code

The real power is using auth to **protect your views**. Here's how:

#### Method 1: Require Login (Decorator)

In `views.py`, add `@login_required` to any view:

```python
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required  # User must be logged in!
def my_protected_view(request):
    return JsonResponse({"message": f"Hello {request.user.username}!"})
```

If someone not logged in tries to access this, Django redirects them to the login page.

#### Method 2: Check Login in Code

```python
def some_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.username})
    else:
        return JsonResponse({"error": "Please login"}, status=401)
```

#### Method 3: Check Permissions

Django has a permission system for each model:

```python
from django.contrib.auth.decorators import permission_required

# Only users with 'add_student' permission can access
@permission_required('api.add_student', raise_exception=True)
def create_student_protected(request):
    # Only superusers/staff with permission can reach here
    pass
```

#### Method 4: API with Session Authentication

For APIs, you can use Django's session auth (browser cookies):

```python
def api_get_user(request):
    """Returns current user info if logged in"""
    if request.user.is_authenticated:
        return JsonResponse({
            "username": request.user.username,
            "email": request.user.email,
            "is_staff": request.user.is_staff,
        })
    return JsonResponse({"error": "Not authenticated"}, status=401)
```

Test it with curl (you need to be logged in via browser first, or use session cookies):

```bash
# This won't work without login
curl http://localhost:8000/api/user/

# Login first via browser at /admin/login/
# Then the same request works with browser cookies
```

### Built-in Login/Logout Views

Django gives you login/logout views for free. Add to `config/urls.py`:

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... your other URLs ...
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

Now visit:
- `/login/` - Django's built-in login form
- `/logout/` - Logs you out

**No code to write!** Django provides the forms, validation, and session handling.

### Summary: Auth Features

| Feature | How to Use | Where |
|---------|-----------|-------|
| Login required | `@login_required` decorator | On any view |
| Check if logged in | `request.user.is_authenticated` | In view code |
| Get current user | `request.user` | In any view |
| Check permissions | `@permission_required('app.action_model')` | On views |
| Built-in login form | `auth_views.LoginView` | In urls.py |
| Built-in logout | `auth_views.LogoutView` | In urls.py |

---

### Exercise: Protect the Students API with Login

Let's add authentication to the API step by step:

#### Step 1: Add Login URLs (Already Done!)

Check `config/urls.py` - the login/logout URLs are already configured:

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    # ... other URLs
]
```

#### Step 2: Uncomment @login_required in the View

Open `api/views.py` and look for the commented lines:

```python
# UNCOMMENT FOR AUTH EXERCISE:
# from django.contrib.auth.decorators import login_required
```

Change to:
```python
# UNCOMMENT FOR AUTH EXERCISE:
from django.contrib.auth.decorators import login_required
```

Then find:
```python
# UNCOMMENT FOR AUTH EXERCISE (add above @csrf_exempt):
# @login_required
@csrf_exempt
```

Change to:
```python
# UNCOMMENT FOR AUTH EXERCISE (add above @csrf_exempt):
@login_required
@csrf_exempt
```

**Important:** `@login_required` must be **above** `@csrf_exempt` (closest to the function).

#### Step 3: Restart the Server

Press `Ctrl+C` to stop the server, then:

```bash
python3 manage.py runserver
```

#### Step 4: Test Without Login

Try accessing the API:

```bash
curl http://localhost:8000/api/students/
```

**Result:** You'll be redirected to `/accounts/login/` (or see a 404 if login URL isn't configured).

In browser, you'll see the login form:

![Login page at /accounts/login/](http://localhost:8000/accounts/login/)

#### Step 5: Login and Test

1. Visit: http://localhost:8000/accounts/login/
2. Enter your superuser credentials (created earlier with `createsuperuser`)
3. After login, visit: http://localhost:8000/api/students/
4. **Now it works!** The API returns JSON because you're authenticated.

#### Step 6: Logout

Visit: http://localhost:8000/accounts/logout/

Now try the API again - it will redirect to login.

---

### How It Works

```
User visits /api/students/
         ↓
@login_required checks: Is user logged in?
         ↓
    NO → Redirect to /accounts/login/
         ↓
    User enters username/password
         ↓
    Django validates → Creates session cookie
         ↓
    Redirect back to /api/students/
         ↓
    YES → Run the view function
         ↓
    Return JSON response
```

---

## Chapter 6: Testing the API

Your Django app has REST API endpoints. Test them with curl **(before adding @login_required)**:

```bash
# Get all students (works without auth)
curl http://localhost:8000/api/students/

# Create a new student
curl -X POST http://localhost:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie", "email": "charlie@iitc.org", "role": "student"}'

# Get stats
curl http://localhost:8000/api/stats/
```

Or visit in your browser:
- http://localhost:8000/api/students/
- http://localhost:8000/api/stats/

---

### Testing After Adding Authentication

**Important:** After you add `@login_required` in Chapter 5, curl will **not work** because it doesn't have a session cookie. The API will return the login page HTML instead of JSON.

**To test with auth enabled:**

1. **Use the browser** (recommended for learning):
   - Login at http://localhost:8000/accounts/login/
   - Then visit http://localhost:8000/api/students/ in the same browser tab
   - You'll see JSON because the browser sends the session cookie

2. **For curl with auth** (advanced), you'd need to:
   - Use a tool like Postman, or
   - Use token-based auth (not covered in this basic lab)

**Remember:** `@login_required` is for browser-based workflows where users login and use the site. For API-only access (like mobile apps), you'd use Token Authentication or JWT instead.

---

## Chapter 7: Unit Testing with Django

### Django Has Built-in Testing

Django includes a test framework based on Python's `unittest`. No extra packages needed!

### Run the Included Tests

A test file `api/tests.py` is included. Run it:

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test -v 2

# Run specific test file
python manage.py test api.tests

# Run specific test class
python manage.py test api.tests.StudentAPITests
```

### What the Tests Cover

The included tests verify:
- ✅ Student model creation and string representation
- ✅ Email uniqueness constraint
- ✅ GET /api/students/ returns list
- ✅ POST /api/students/ creates student
- ✅ GET /api/students/{id}/ returns single student
- ✅ PUT /api/students/{id}/ updates student
- ✅ DELETE /api/students/{id}/ removes student
- ✅ Admin login works

### Key Django Testing Features

**Test Database:** Django automatically creates a test database:
```python
class StudentAPITests(TestCase):
    def setUp(self):
        # This runs before each test
        Student.objects.create(name="Test", email="test@example.com")
    
    def test_something(self):
        # Tests run with fresh test data
        self.assertEqual(Student.objects.count(), 1)
```

**Test Client:** Simulate HTTP requests:
```python
def test_api(self):
    client = Client()
    response = client.get('/api/students/')
    self.assertEqual(response.status_code, 200)
```

### Learn More

See `../LAB_Testing.md` for comprehensive testing guide covering:
- pytest fundamentals
- Fixtures and mocking
- Testing Flask and FastAPI apps
- Test organization best practices

---

## Quick Reference: ORM Cheat Sheet

| What You Want | How to Do It |
|---------------|--------------|
| Create one | `Student.objects.create(name="X", email="Y")` |
| Get all | `Student.objects.all()` |
| Filter | `Student.objects.filter(role="student")` |
| Get one | `Student.objects.get(id=1)` |
| Count | `Student.objects.count()` |
| Update | `s = Student.objects.get(id=1); s.name = "New"; s.save()` |
| Delete | `s = Student.objects.get(id=1); s.delete()` |
| Order by | `Student.objects.order_by("name")` |
| Reverse order | `Student.objects.order_by("-created_at")` |

---

## Summary: Flask vs Django

| Feature | Flask | Django |
|---------|-------|--------|
| Philosophy | "Do it yourself" | "Batteries included" |
| Database | Bring your own | Built-in ORM |
| Admin panel | Build yourself | Auto-generated |
| User auth | Build yourself | Built-in |
| Learning curve | Easier to start | More to learn upfront |
| Best for | Small apps, learning | Full production apps |

**Remember:**
- Flask gives you freedom. Django gives you speed.
- In Flask, you write more code but control everything.
- In Django, much is pre-built, but you follow Django's rules.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No such table" error | Run `python3 manage.py migrate` |
| "No module named django" | Activate venv: `source venv/bin/activate` |
| Can't login to admin | Create superuser: `python3 manage.py createsuperuser` |
| Changes not showing | Restart the server (Ctrl+C, then run again) |

---

## Next Steps

1. **Explore the code:** Look at `api/models.py`, `api/views.py`, `api/admin.py`
2. **Add a field:** Edit `models.py`, then run `makemigrations` and `migrate`
3. **Customize the admin:** Edit `admin.py` to change what columns show
4. **Build a new endpoint:** Add a URL in `urls.py` and a view in `views.py`
