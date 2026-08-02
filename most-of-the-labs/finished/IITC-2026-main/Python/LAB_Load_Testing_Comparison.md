# Load Testing Lab — Flask vs Django vs FastAPI Performance Battle

> **Goal:** Compare how each framework handles high traffic using real load tests.

---

## Prerequisites

Install load testing tools:

```bash
# Mac
brew install apache2-utils  # For 'ab' command
brew install wrk             # For 'wrk' command (better)

# Ubuntu/Debian
sudo apt-get install apache2-utils
sudo apt-get install wrk

# All platforms
pip install locust
```

---

## Chapter 1: The Test Setup

### What We're Testing

Each framework serves the same `/students` endpoint. We'll measure:

| Metric | What it means |
|--------|---------------|
| **Requests/sec** | How many requests the server handles per second |
| **Latency** | Time to respond (lower is better) |
| **Failed requests** | Requests that timeout or error |
| **CPU/Memory** | System resources used |

### Start All Three Servers

**Terminal 1 — Flask:**
```bash
cd flask_app
source venv/bin/activate
python3 app.py
# Running on http://localhost:5000
```

**Terminal 2 — Django:**
```bash
cd django_app
source venv/bin/activate
python3 manage.py runserver
# Running on http://localhost:8000
```

**Terminal 3 — FastAPI:**
```bash
cd fastapi_app
source venv/bin/activate
uvicorn main:app --reload
# Running on http://localhost:8000
```

---

## Chapter 2: Basic Load Test with `ab`

### Test 1: Single Request (Baseline)

```bash
# Flask
time curl http://localhost:5000/students

# Django
time curl http://localhost:8000/api/students/

# FastAPI (change port if Django is on 8000)
time curl http://localhost:8000/students
```

**Expected:** All should be fast (~10-50ms) for single requests.

### Test 2: 100 Requests, 1 Concurrent (Sequential)

```bash
# Flask
ab -n 100 -c 1 http://localhost:5000/students

# Django
ab -n 100 -c 1 http://localhost:8000/api/students/

# FastAPI (change port if needed)
ab -n 100 -c 1 http://localhost:8000/students
```

**What to look for:**
```
Requests per second:    XXX.XX [#/sec] (mean)
Time per request:       X.XXX [ms] (mean)
Failed requests:        0
```

### Test 3: 1000 Requests, 10 Concurrent (Light Load)

```bash
# Flask - WARNING: Will be slow!
ab -n 1000 -c 10 http://localhost:5000/students

# Django - WARNING: Will be slow!
ab -n 1000 -c 10 http://localhost:8000/api/students/

# FastAPI
ab -n 1000 -c 10 http://localhost:8000/students
```

**Expected Results:**

| Framework | Requests/sec | Time/req | Notes |
|-----------|--------------|----------|-------|
| **Flask** | ~50-100 | ~100ms | Synchronous - 1 at a time |
| **Django** | ~50-100 | ~100ms | Synchronous - 1 at a time |
| **FastAPI** | ~500-2000 | ~5-20ms | Async - handles many at once |

**Why the difference?**
- Flask/Django (WSGI): Each request blocks until complete
- FastAPI (ASGI): Uses `async` to handle multiple requests concurrently

---

## Chapter 3: Heavy Load Test with `wrk`

`wrk` is more realistic than `ab` — it uses fewer resources and gives better results.

### Test 4: Sustained Heavy Load (30 seconds)

```bash
# Flask - WARNING: Will struggle!
wrk -t12 -c400 -d30s http://localhost:5000/students

# Django - WARNING: Will struggle!
wrk -t12 -c400 -d30s http://localhost:8000/api/students/

# FastAPI
wrk -t12 -c400 -d30s http://localhost:8000/students
```

**Parameters explained:**
- `-t12` = 12 threads (for generating load)
- `-c400` = 400 concurrent connections
- `-d30s` = Test for 30 seconds

**Expected Results:**

| Framework | Requests/sec | Avg Latency | Max Latency |
|-----------|--------------|-------------|-------------|
| **Flask** | ~100-200 | ~500ms | ~5000ms |
| **Django** | ~100-200 | ~500ms | ~5000ms |
| **FastAPI** | ~2000-5000 | ~50ms | ~200ms |

**Key observation:** FastAPI's max latency stays low even under heavy load.

### Test 5: Monitor While Testing

**Terminal 4 — Monitor Flask:**
```bash
# While wrk is running against Flask:
watch -n 1 'ps aux | grep python | grep -v grep'
```

You'll see Flask using 100% of one CPU core.

**Terminal 4 — Monitor FastAPI:**
```bash
# While wrk is running against FastAPI:
watch -n 1 'ps aux | grep uvicorn | grep -v grep'
```

FastAPI will distribute load better with async.

---

## Chapter 4: Realistic Scenario with Locust

Locust lets you define user behavior and simulates real traffic patterns.

### Create `locustfile.py`

```python
from locust import HttpUser, task, between

class FlaskUser(HttpUser):
    """Simulate user hitting Flask app"""
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    host = "http://localhost:5000"
    
    @task
    def get_students(self):
        self.client.get("/students")
    
    @task(2)  # 2x more frequent
    def get_home(self):
        self.client.get("/")

class DjangoUser(HttpUser):
    """Simulate user hitting Django app"""
    wait_time = between(1, 3)
    host = "http://localhost:8000"
    
    @task
    def get_students(self):
        self.client.get("/api/students/")
    
    @task(2)
    def get_home(self):
        self.client.get("/admin/")  # Test admin too

class FastAPIUser(HttpUser):
    """Simulate user hitting FastAPI app"""
    wait_time = between(1, 3)
    host = "http://localhost:8000"
    
    @task(3)  # Even more frequent - it's fast!
    def get_students(self):
        self.client.get("/students")
    
    @task
    def create_student(self):
        self.client.post("/students", json={
            "name": "Load Test",
            "email": f"load{self.user_id}@test.com",
            "role": "student"
        })
```

### Run the Load Test

**Step 1:** Start Locust web UI:
```bash
# Make sure all three servers are running first!
locust -f locustfile.py
```

**Step 2:** Open browser:
```
http://localhost:8089
```

**Step 3:** Configure test:
- Number of users: 100
- Spawn rate: 10 users/second
- Host: Pick one (http://localhost:5000 for Flask, etc.)

**Step 4:** Start and watch the graphs!

### Compare Results

Run three separate tests (one per framework) and compare:

| Metric | Flask | Django | FastAPI |
|--------|-------|--------|---------|
| **Response Time (median)** | ~200ms | ~200ms | ~20ms |
| **Response Time (95th %ile)** | ~800ms | ~800ms | ~50ms |
| **Requests/sec** | ~200 | ~200 | ~2000+ |
| **Failed Requests** | 0-5% | 0-5% | 0% |
| **CPU Usage** | 100% | 100% | ~20% |

---

## Chapter 5: The Multi-Worker Test

### Flask with Gunicorn

**Stop the Flask dev server, start with workers:**
```bash
cd flask_app
source venv/bin/activate
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Now test again:
```bash
wrk -t12 -c400 -d30s http://localhost:5000/students
```

**Result:** 4x better than single Flask worker (but still slower than FastAPI).

### Django with Gunicorn

```bash
cd django_app
source venv/bin/activate
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 config.wsgi:application
```

Test:
```bash
wrk -t12 -c400 -d30s http://localhost:8000/api/students/
```

### FastAPI with Multiple Workers

```bash
cd fastapi_app
source venv/bin/activate
uvicorn main:app --workers 4 --port 8000
```

Test:
```bash
wrk -t12 -c400 -d30s http://localhost:8000/students
```

### Comparison: 4 Workers Each

| Framework | Workers | Requests/sec | Efficiency |
|-----------|---------|--------------|------------|
| **Flask** | 4 | ~800 | Low (sync) |
| **Django** | 4 | ~800 | Low (sync) |
| **FastAPI** | 4 | ~8000-20000 | High (async) |

**Why FastAPI is still faster:**
- Flask/Django workers handle 1 request at a time
- FastAPI workers handle 100s concurrently using async

---

## Chapter 6: Understanding the Results

### What the Numbers Mean

**Requests/sec:**
- Flask: ~200 → Can serve 200 students/second
- FastAPI: ~2000 → Can serve 2000 students/second
- **10x difference!**

**Latency (Response Time):**
- Flask: ~500ms → User waits half a second
- FastAPI: ~20ms → User barely notices
- **25x difference!**

**Failed Requests:**
- Flask: Starts failing at ~100 concurrent users
- FastAPI: Handles 1000+ concurrent users easily

### When Does It Matter?

| Scenario | Flask/Django OK? | FastAPI Better? |
|----------|------------------|-----------------|
| < 10 users | ✅ Yes | Not needed |
| < 100 users | ✅ Yes | ✅ Better |
| < 1000 users | ⚠️ Maybe | ✅ Yes |
| > 1000 users | ❌ No | ✅ Yes |
| Real-time chat | ❌ No | ✅ Yes |
| Streaming data | ❌ No | ✅ Yes |

### The Real Cost

**If you have 1000 users:**

**Flask/Django:**
- Need 20-50 servers
- Each server handles ~20-50 requests/sec
- Expensive infrastructure

**FastAPI:**
- Need 2-5 servers
- Each server handles ~500-1000 requests/sec
- Cheaper infrastructure

---

## Chapter 7: Script for Automated Comparison

Create `compare_frameworks.sh`:

```bash
#!/bin/bash
# Automated comparison script
# Usage: ./compare_frameworks.sh

echo "=== Framework Load Test Comparison ==="
echo

# Function to test a URL
test_url() {
    local name=$1
    local url=$2
    
    echo "Testing $name: $url"
    echo "Running: ab -n 1000 -c 10"
    
    # Run ab and extract key metrics
    ab -n 1000 -c 10 "$url" 2>&1 | grep -E "(Requests per second|Time per request|Failed requests)"
    echo
}

# Test each framework
test_url "Flask" "http://localhost:5000/students"
test_url "Django" "http://localhost:8000/api/students/"
test_url "FastAPI" "http://localhost:8000/students"

echo "=== Comparison Complete ==="
echo "Winner is the one with:"
echo "  - Highest Requests/sec"
echo "  - Lowest Time per request"
echo "  - Zero Failed requests"
```

Make executable and run:
```bash
chmod +x compare_frameworks.sh
./compare_frameworks.sh
```

---

## Summary: The Verdict

| Test | Flask | Django | FastAPI |
|------|-------|--------|---------|
| 1 user (latency) | ✅ Fast | ✅ Fast | ✅ Fast |
| 10 concurrent | ⚠️ OK | ⚠️ OK | ✅ Fast |
| 100 concurrent | ❌ Slow | ❌ Slow | ✅ Fast |
| 1000 concurrent | ❌ Fails | ❌ Fails | ✅ Fast |
| Resource usage | ❌ High | ❌ High | ✅ Low |
| Ease of scaling | ⚠️ Workers | ⚠️ Workers | ✅ Async |

### Key Takeaways

1. **For learning/small apps:** Any framework works
2. **For production APIs:** FastAPI handles 10x more traffic
3. **Flask/Django need:** Multiple workers + load balancer
4. **FastAPI needs:** Fewer workers, simpler infrastructure
5. **The secret:** `async` lets one worker do the work of many

---

## Quick Reference: Load Testing Commands

```bash
# Basic test
ab -n 100 -c 10 <url>

# Heavy test
ab -n 1000 -c 100 <url>

# Better tool
wrk -t12 -c400 -d30s <url>

# Realistic user simulation
locust -f locustfile.py

# Monitor during test
watch -n 1 'ps aux | grep python'
```
