"""
=============================================================================
FLASK — Micro Web Framework
=============================================================================

WHAT IS FLASK?
Flask is a "micro" framework — it gives you the bare minimum to build a web
app and leaves every other decision to you.

HOW DOES IT WORK BEHIND THE SCENES?
1. Flask is a WSGI application. WSGI (Web Server Gateway Interface) is a
   Python standard (PEP 3333) that defines how a web server talks to a
   Python app.

2. When you run `python app.py`, Flask starts a built-in development server
   (Werkzeug). In production, you'd use Gunicorn or uWSGI instead.

3. The request lifecycle:
   Browser sends HTTP request
       → Werkzeug/Gunicorn receives raw bytes
       → Parses into a WSGI environ dict
       → Calls your Flask app: app(environ, start_response)
       → Flask matches the URL to a route function
       → Route function returns a Response object
       → Werkzeug sends the HTTP response bytes back

4. Flask is SYNCHRONOUS by default.
   Each request blocks until the function returns.
   If your handler sleeps for 1 second, that worker is frozen for 1 second.
   To scale, you run multiple worker processes (gunicorn -w 4).

WHEN TO USE FLASK:
- Learning how web frameworks work (minimal magic)
- Small REST APIs or microservices
- Quick prototypes
- When you want full control over every component

WHEN NOT TO USE FLASK:
- Large team projects (no enforced structure = messy code)
- Apps needing built-in auth, admin panel, ORM (Django does this better)
- High-concurrency async workloads (FastAPI does this better)
=============================================================================
"""

from flask import Flask, request, jsonify, render_template, abort

# ---------------------------------------------------------------------------
# 1. The Application Object
# ---------------------------------------------------------------------------
# Flask(__name__) creates the WSGI application object.
# __name__ tells Flask where to look for templates and static files.
# This single object IS your web application.

app = Flask(__name__)


# ---------------------------------------------------------------------------
# 2. How Routing Works
# ---------------------------------------------------------------------------
# @app.route() is a decorator that registers a URL rule in Flask's internal
# URL map (a Werkzeug Map object).
#
# When a request comes in, Flask calls url_map.bind(environ).match() which
# uses Werkzeug's routing algorithm to find the matching endpoint.
#
# The "endpoint" is the name of the function (by default). Flask then calls
# that function and expects a string, dict, Response, or tuple back.

@app.route("/")
def index():
    """
    The simplest possible route.
    Returning a string → Flask wraps it in a 200 OK Response with
    Content-Type: text/html automatically.
    """
    return render_template("index.html")


# ---------------------------------------------------------------------------
# 3. URL Parameters
# ---------------------------------------------------------------------------
# <name> in the route string is a variable rule.
# Flask extracts it from the URL path and passes it as a keyword argument.
# <int:user_id> uses a built-in converter that validates and casts to int.
# Other converters: str (default), float, path, uuid

@app.route("/users/<int:user_id>")
def get_user(user_id):
    """
    Demonstrates URL path parameters and JSON responses.

    jsonify() creates a Response with Content-Type: application/json
    and serializes the dict using Python's json module.
    """
    # Simulated in-memory data (no database in this example)
    users = {
        1: {"id": 1, "name": "Alice", "role": "admin"},
        2: {"id": 2, "name": "Bob",   "role": "student"},
    }

    user = users.get(user_id)
    if not user:
        # abort() raises an HTTPException which Flask catches and converts
        # to the appropriate HTTP error response (404 Not Found here)
        abort(404, description=f"User {user_id} not found")

    return jsonify(user)


# ---------------------------------------------------------------------------
# 4. HTTP Methods
# ---------------------------------------------------------------------------
# By default, routes only accept GET. You must explicitly allow other methods.
# Flask will return 405 Method Not Allowed automatically for disallowed methods.

@app.route("/users", methods=["GET", "POST"])
def users():
    """
    GET  /users  → list all users
    POST /users  → create a new user

    request is a thread-local proxy object — it points to the current
    request being handled. Flask pushes a new request context onto a
    stack at the start of each request and pops it at the end.
    This is why you can import `request` globally yet it always refers
    to the current request: it's a context-local proxy, not a global.
    """
    if request.method == "GET":
        # request.args is a MultiDict of query string parameters
        # e.g. /users?role=admin → request.args.get("role") == "admin"
        role_filter = request.args.get("role")

        all_users = [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob",   "role": "student"},
            {"id": 3, "name": "Carol", "role": "student"},
        ]

        if role_filter:
            all_users = [u for u in all_users if u["role"] == role_filter]

        return jsonify(all_users)

    elif request.method == "POST":
        # request.get_json() parses the request body as JSON.
        # Returns None if Content-Type is not application/json or body is invalid.
        data = request.get_json()

        if not data or "name" not in data:
            # Returning a tuple (response, status_code) is a Flask shortcut
            return jsonify({"error": "name is required"}), 400

        new_user = {"id": 99, "name": data["name"], "role": data.get("role", "student")}
        # 201 Created is the correct HTTP status for a successful resource creation
        return jsonify(new_user), 201


# ---------------------------------------------------------------------------
# 5. Middleware — Before & After Request Hooks
# ---------------------------------------------------------------------------
# Flask doesn't have traditional middleware classes (like Django or FastAPI).
# Instead, it uses hooks that run before/after every request in the app context.
#
# Behind the scenes, Flask maintains a list of these functions and calls them
# in registration order at the appropriate point in the request lifecycle.

@app.before_request
def log_request_start():
    """
    Runs before EVERY request handler.
    Common uses: authentication checks, logging, rate limiting.

    If this function returns a value (not None), Flask uses that as the
    response and skips the actual route handler entirely — useful for
    early auth rejection.
    """
    print(f"[FLASK] Incoming: {request.method} {request.path}")


@app.after_request
def add_headers(response):
    """
    Runs after EVERY request handler, receives the Response object.
    Must return a Response object.
    Common uses: adding CORS headers, setting cookies, logging response time.
    """
    response.headers["X-Powered-By"] = "Flask Educational App"
    return response


# ---------------------------------------------------------------------------
# 6. Error Handlers
# ---------------------------------------------------------------------------
# Register custom handlers for specific HTTP error codes.
# Flask calls these when abort(code) is raised or an exception occurs.

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal Server Error"}), 500


# ---------------------------------------------------------------------------
# 7. A Route That Demonstrates the Request/Response Cycle Clearly
# ---------------------------------------------------------------------------

@app.route("/echo", methods=["POST"])
def echo():
    """
    Echoes back everything Flask parsed from the incoming request.
    Use this to understand what Flask gives you from a raw HTTP request.
    """
    return jsonify({
        "method":      request.method,
        "path":        request.path,
        "headers":     dict(request.headers),
        "query_args":  dict(request.args),
        "json_body":   request.get_json(silent=True),  # silent=True won't raise on bad JSON
        "form_data":   dict(request.form),
    })


# ---------------------------------------------------------------------------
# 8. EXERCISES (Uncomment for Lab Chapters 6 & 7)
# ---------------------------------------------------------------------------

# UNCOMMENT FOR VALIDATION EXERCISE (Chapter 6):
# First install: pip install marshmallow
# from marshmallow import Schema, fields, validate, ValidationError
#
# class StudentSchema(Schema):
#     name = fields.Str(required=True, validate=validate.Length(min=2))
#     email = fields.Email(required=True)
#     role = fields.Str(validate=validate.OneOf(['student', 'teacher', 'admin']))
#
# student_schema = StudentSchema()
#
# @app.route('/api/students-validated', methods=['POST'])
# def create_student_validated():
#     """Example with automatic validation using marshmallow"""
#     try:
#         data = student_schema.load(request.get_json())
#         return jsonify({"success": True, "data": data}), 201
#     except ValidationError as err:
#         return jsonify({"errors": err.messages}), 400


# UNCOMMENT FOR BLUEPRINT EXERCISE (Chapter 7):
# from flask import Blueprint
#
# # Create a blueprint for API versioning
# api_bp = Blueprint('api', __name__, url_prefix='/api/v2')
#
# @api_bp.route('/students')
# def api_v2_students():
#     """Same data, different URL structure via blueprint"""
#     return jsonify({
#         "version": "2.0",
#         "students": list(_users_db.values())
#     })
#
# # Register blueprint in main app (add this before app.run()):
# # app.register_blueprint(api_bp)


# ---------------------------------------------------------------------------
# 9. Entry Point
# ---------------------------------------------------------------------------
# When you run `python app.py`, Python sets __name__ to "__main__".
# app.run() starts Werkzeug's built-in development server.
#
# debug=True enables:
#   - Automatic reloader (watches files, restarts on change)
#   - Interactive debugger in the browser on exceptions
#   - Detailed error pages
#
# NEVER use debug=True in production — it exposes your code to arbitrary execution.

if __name__ == "__main__":
    print("Starting Flask development server...")
    print("Visit: http://localhost:5000")
    print("Try:   http://localhost:5000/users")
    print("Try:   http://localhost:5000/users/1")
    app.run(debug=True, port=5000)
