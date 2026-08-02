# Flask Lab: Simplicity and Control — A Beginner's Journey

> **Welcome to Flask.**
>
> Flask is the simplest Python web framework. You write everything yourself,
> which makes it perfect for learning how web frameworks actually work.

---

## The Story: The Mechanic's Workshop

Imagine you're learning to build cars:

**Flask is like an empty workshop:**
- You have basic tools (routing, requests, responses)
- You decide how to organize everything
- You build each component yourself
- You learn deeply because there's no magic hiding how things work

**Django is like a car factory:**
- Everything is pre-built and automated
- You customize the existing systems
- Fast production, but less understanding of internals

**FastAPI is like a race car garage:**
- Built for speed and performance
- Modern tools and automation
- Great for specific use cases

---

## Chapter 1: Why Start with Flask?

### The Philosophy: "Explicit is Better Than Implicit"

Flask shows you exactly what's happening:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/students', methods=['GET'])
def get_students():
    # You write the query logic
    students = db.query_all()
    # You format the response
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
```

**What you see is what you get.** No hidden magic.

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
cd Python\flask_app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Setup Commands (macOS/Linux/Git Bash)

```bash
# 1. Navigate to Flask project
cd Python/flask_app

# 2. Create virtual environment (first time only)
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python3 app.py

# Server starts at http://localhost:5000
```

---

## Chapter 2: Your First Flask App

### Understanding the Structure

Open `app.py` and look at the basic structure:

```python
# 1. Import Flask
from flask import Flask, jsonify, request, render_template

# 2. Create the app instance
app = Flask(__name__)

# 3. Define routes
@app.route('/')
def home():
    return 'Hello, World!'

# 4. Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

**The Pattern:**
1. **Import** - Bring in what you need
2. **Create app** - `Flask(__name__)` creates your application
3. **Add routes** - `@app.route()` maps URLs to functions
4. **Run** - `app.run()` starts the server

**What happens when you run `app.run()`?**

Flask starts a development server called **Werkzeug** (German for "tool"). It:
1. Listens for HTTP requests on port 5000
2. Matches URLs to your Python functions
3. Returns responses back to the browser

**What is WSGI?**
WSGI = Web Server Gateway Interface

Think of it like a **waiter** at a restaurant:
- **Takes orders** from customers (HTTP requests from browsers)
- **Brings orders to the kitchen** (your Python code)
- **Delivers food back** (HTTP responses)

Flask is a **WSGI application** - it speaks the WSGI "language" to communicate with web servers. This is why Flask is synchronous (one request at a time per worker).

---

## Chapter 3: Routing and Request Handling

### Exercise: Test the Existing Routes

With the server running, test these URLs in your browser:

1. **Home:** http://localhost:5000/
2. **API Students:** http://localhost:5000/api/students
3. **HTML Page:** http://localhost:5000/students

### Exercise: Add a New Route

Add this to `app.py` (find a good spot near other routes):

```python
@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello, {name}!'
```

Restart the server (`Ctrl+C`, then `python3 app.py` again)

Test: http://localhost:5000/hello/Alice

**What happened?**
- `<name>` in the URL pattern becomes a variable
- Flask passes 'Alice' as the `name` parameter
- You return a response using that variable

---

## Chapter 4: Handling Different HTTP Methods

### GET vs POST

**GET** - Read data:
```python
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)
```

**POST** - Create data:
```python
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()  # Read JSON body
    # Add to database...
    return jsonify(new_student), 201
```

### Exercise: Test with curl

```bash
# GET request
curl http://localhost:5000/api/students

# POST request
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com"}'
```

---

## Chapter 5: Templates (HTML Rendering)

### Exercise: Explore Templates

Look in the `templates/` folder. You'll find HTML files.

Flask uses **Jinja2** for templating:

```html
<!-- In template -->
<h1>Hello, {{ name }}!</h1>

{% for student in students %}
  <p>{{ student.name }}</p>
{% endfor %}
```

```python
# In app.py
@app.route('/students')
def students_page():
    return render_template('students.html', students=students)
```

Visit http://localhost:5000/students to see it in action.

---

## Chapter 6: Manual Validation (vs FastAPI's Automatic)

### The Flask Way

In Flask, you write validation yourself:

```python
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    
    # Manual validation
    if not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    if len(data['name']) < 2:
        return jsonify({"error": "Name too short"}), 400
    
    # Process if valid
    # ...
```

**Compare to FastAPI:** FastAPI does this automatically from type hints. Flask gives you control but requires more code.

### UNCOMMENT FOR VALIDATION EXERCISE:

In `app.py`, find this commented section and uncomment it:

```python
# UNCOMMENT FOR VALIDATION EXERCISE:
# from marshmallow import Schema, fields, validate, ValidationError
#
# class StudentSchema(Schema):
#     name = fields.Str(required=True, validate=validate.Length(min=2))
#     email = fields.Email(required=True)
#     role = fields.Str(validate=validate.OneOf(['student', 'teacher', 'admin']))
#
# student_schema = StudentSchema()
```

Then find and uncomment the validated endpoint:

```python
# UNCOMMENT FOR VALIDATION EXERCISE:
# @app.route('/api/students-validated', methods=['POST'])
# def create_student_validated():
#     """Example with automatic validation using marshmallow"""
#     try:
#         data = student_schema.load(request.get_json())
#         # data is now validated and parsed
#         return jsonify({"success": True, "data": data}), 201
#     except ValidationError as err:
#         return jsonify({"errors": err.messages}), 400
```

**Install marshmallow:**
```bash
pip install marshmallow
```

Now test:
```bash
curl -X POST http://localhost:5000/api/students-validated \
  -H "Content-Type: application/json" \
  -d '{"name": "A", "email": "invalid-email"}'
```

**Result:** Proper validation errors like FastAPI!

---

## Chapter 7: Blueprints — Organizing Larger Apps

### The Problem

As your app grows, `app.py` becomes huge. Flask Blueprints help you organize:

```python
# UNCOMMENT FOR BLUEPRINT EXERCISE:
# from flask import Blueprint
#
# # Create a blueprint
# api_bp = Blueprint('api', __name__, url_prefix='/api/v2')
#
# # Add routes to blueprint
# @api_bp.route('/students')
# def api_students():
#     return jsonify(students)
#
# # Register blueprint in main app
# app.register_blueprint(api_bp)
```

Find and uncomment the blueprint exercise code in `app.py`, then test:
http://localhost:5000/api/v2/students

---

## Chapter 8: Testing Flask Applications

### Run the Included Tests

A test file `test_app.py` is included. Run it:

```bash
# Install pytest (already in requirements.txt)
pip install pytest

# Run all tests
pytest test_app.py -v
```

### What's Being Tested

The included tests verify:
- ✅ Home page loads (200 OK)
- ✅ GET /api/students returns JSON list
- ✅ POST /api/students creates new student
- ✅ GET /users/1 returns a user
- ✅ GET /users/9999 returns 404

### The Test Client

Flask provides `test_client()` that simulates HTTP requests without running a real server:

```python
from app import app

def test_home():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
```

### Learn More

See `../LAB_Testing.md` for comprehensive testing guide covering:
- pytest fundamentals
- Fixtures and setup/teardown
- Mocking external services
- Testing Django and FastAPI apps

---

## Quick Reference: Flask Cheat Sheet

| What You Want | How to Do It |
|---------------|--------------|
| Create route | `@app.route('/path')` |
| Route with parameter | `@app.route('/user/<id>')` |
| POST only | `@app.route('/path', methods=['POST'])` |
| Get JSON body | `request.get_json()` |
| Get query params | `request.args.get('key')` |
| Return JSON | `jsonify(data)` |
| Return HTML | `render_template('file.html', var=value)` |
| Set status code | `return data, 201` |
| Run app | `app.run(debug=True)` |

---

## Summary: Flask vs Django vs FastAPI

| Feature | Flask | Django | FastAPI |
|---------|-------|--------|---------|
| **Philosophy** | "Do it yourself" | "Batteries included" | "Fast & type-safe" |
| **Code Required** | **More** (manual) | Less (built-in) | Less (auto-generated) |
| **Learning Value** | **Best** (no magic) | Good (conventions) | Good (modern patterns) |
| **Flexibility** | **Maximum** | Opinionated | Flexible |
| **Best for** | **Learning**, small apps | Full web apps | High-performance APIs |

**Why learn Flask first?**
1. You understand every piece of your app
2. No hidden "magic" - you see how data flows
3. Easy to move to Django/FastAPI after
4. Perfect for prototyping and small projects

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named flask" | Activate venv: `source venv/bin/activate` |
| Port already in use | `lsof -ti:5000 \| xargs kill -9` then restart |
| Changes not showing | Stop and restart: `Ctrl+C`, then `python3 app.py` |
| Template not found | Check `templates/` folder is in the same directory as `app.py` |

---

## Next Steps

1. **Add a database:** Replace in-memory list with SQLite using SQLAlchemy
2. **Add authentication:** Use Flask-Login for user sessions
3. **Add forms:** Use Flask-WTF for form handling
4. **Deploy:** Try Flask on PythonAnywhere (free hosting)
