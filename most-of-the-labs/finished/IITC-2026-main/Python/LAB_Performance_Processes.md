# Performance, Processes & Threads Lab — Linux Deep Dive

> **Why learn this?** Web apps run on servers. Understanding processes, threads, and performance helps you debug slow apps and scale properly.

---

## Chapter 1: Process vs Thread — The Restaurant Analogy

| | Process (Entire Restaurant) | Thread (Individual Chef) |
|---|---|---|
| **Memory** | Own building | Shares kitchen |
| **Isolation** | Crash doesn't affect others | Crash kills whole restaurant |
| **Creation cost** | Expensive (needs building) | Cheap (just hire chef) |
| **Communication** | Slow (phone orders) | Fast (shout in kitchen) |
| **Best for** | CPU-heavy tasks | I/O-heavy tasks |

**Python's GIL Problem:**
- Python can only run **one thread** at a time (GIL = Global Interpreter Lock)
- For CPU-heavy work, use **processes** (multiprocessing)
- For I/O work (network, disk), use **threads** (threading)

---

## Chapter 2: Linux Monitoring Commands

### 1. `ps` — List Processes

```bash
ps aux                    # All processes
ps aux | grep python      # Filter for Python
ps aux | grep uvicorn     # Find your web server
ps -eo pid,pcpu,pmem,comm # Custom columns
```

**Key columns:**
- `PID` — Process ID
- `%CPU` — CPU usage
- `%MEM` — Memory usage
- `STAT` — State (R=running, S=sleeping)

### 2. `top` — Live Process Monitor

```bash
top
# Press M to sort by memory
# Press P to sort by CPU
# Press q to quit
```

**Important line:**
```
load average: 0.52, 0.58, 0.59
```
- Above 1.0 = overloaded (processes waiting for CPU)
- Above number of cores = seriously overloaded

### 3. Check Your Cores

```bash
nproc                    # Number of CPU cores
lscpu | grep "CPU(s)"   # Detailed CPU info
cat /proc/cpuinfo        # All CPU info
```

### 4. `pidstat` — Per-Process Stats

```bash
# Install
sudo apt-get install sysstat  # Ubuntu
brew install sysstat          # Mac

# Watch process 1234 every 2 seconds
pidstat -p 1234 2

# Watch threads (important for async!)
pidstat -t -p 1234 2
```

### 5. `lsof` — What Files/Ports Open?

```bash
lsof -p 1234             # Files opened by process
lsof -i :8000            # What's using port 8000?
lsof -i                  # All network connections
```

### 6. `strace` — What is Process Doing?

```bash
# Trace system calls
sudo strace -p 1234

# Count what it's doing
sudo strace -c -p 1234
```

---

## Chapter 3: Python — Threading vs Multiprocessing

### When to Use What?

| Task Type | Use | Why |
|-----------|-----|-----|
| Web requests, DB queries | **Threading** | Waiting for network, GIL ok |
| Image processing, calculations | **Multiprocessing** | CPU heavy, need true parallelism |

### Exercise 1: Threading for I/O

A file `threading_demo.py` is already created. Run it:

```bash
python3 threading_demo.py
```

**Expected output:**
```
=== Sequential (1 at a time) ===
Total time: 3.0s

=== Threading (all at once) ===
Total time: 1.0s
```

**Observation:** Threading makes I/O-bound tasks 3x faster!

**CHALLENGE:** Open `threading_demo.py` and look for the `# CHALLENGE` comment at the bottom.

### Exercise 2: Multiprocessing for CPU

A file `cpu_demo.py` is already created. Run it:

```bash
python3 cpu_demo.py
```

**Expected output:**
```
CPU cores available: 8

=== Sequential (1 process, 1 after another) ===
Total time: 8.5s

=== Multiprocessing (4 workers) ===
Total time: 2.1s

Speedup: 4.0x faster with multiprocessing!
```

**Observation:** Multiprocessing uses all CPU cores for CPU-bound tasks!

**CHALLENGE:** Open `cpu_demo.py` and look for the `# CHALLENGE` comment at the bottom.

**Result:** Multiprocessing is faster (4x on 4-core CPU) because it bypasses GIL.

---

## Chapter 4: Monitor Your Web Apps

### Exercise: Watch Uvicorn Workers

**Terminal 1:** Start FastAPI with 2 workers
```bash
cd fastapi_app
uvicorn main:app --workers 2
```

**Terminal 2:** Monitor it
```bash
# Find uvicorn processes
ps aux | grep uvicorn
# You should see: 1 master + 2 workers = 3 processes

# Monitor specific process
pidstat -p <WORKER_PID> 2

# See threads (uvicorn uses threads within workers!)
pidstat -t -p <WORKER_PID> 2
```

**Terminal 3:** Generate load
```bash
while true; do curl http://localhost:8000/; done
```

**Watch in Terminal 2:** CPU usage goes up when requests come in.

### Exercise: Compare Flask vs FastAPI Under Load

**Flask (WSGI - synchronous):**
```bash
# Terminal 1: Start Flask
cd flask_app
python3 app.py

# Terminal 2: Load test
ab -n 100 -c 10 http://localhost:5000/
```

**FastAPI (ASGI - asynchronous):**
```bash
# Terminal 1: Start FastAPI
cd fastapi_app
uvicorn main:app

# Terminal 2: Load test
ab -n 100 -c 10 http://localhost:8000/
```

**Compare:**
- Flask handles 1 request at a time per worker
- FastAPI handles many concurrently

---

## Chapter 5: Load Testing Tools

### Apache Bench (`ab`)

```bash
# Install
sudo apt-get install apache2-utils  # Ubuntu
brew install apache2-utils          # Mac

# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8000/

# Key output:
# Requests per second:    1234.56 [#/sec]
# Time per request:       8.101 [ms]
# Failed requests:        0
```

### `wrk` (Modern & Fast)

```bash
# Install
brew install wrk  # Mac

# 12 threads, 400 connections, 30 seconds
wrk -t12 -c400 -d30s http://localhost:8000/
```

### Python Locust (Programmable)

```bash
pip install locust
```

A file `locustfile.py` is already created with 3 test classes (Flask, Django, FastAPI).

Run it:
```bash
locust -f locustfile.py
# Open http://localhost:8089 in browser
```

**Then in the web UI:**
- Pick a user class (FlaskUser, DjangoUser, or FastAPIUser)
- Set number of users: 100
- Set spawn rate: 10
- Click "Start swarming"

**CHALLENGE:** Open `locustfile.py` and look at the `# CHALLENGE` comments at the bottom.

---

## Chapter 6: Profiling Python Code

### 1. Simple Timing

The `time` command measures how long a program takes to run.

**Run it on a demo script:**

```bash
time python3 cpu_demo.py
```

**Understanding the output:**
```
real    0m0.847s   ← Actual wall-clock time (what you experienced)
user    0m2.234s   ← CPU time spent in your Python code
sys     0m0.045s   ← CPU time spent in system calls (OS operations)
```

**What this tells you:**
- **real < user** → The program used multiple CPU cores (multiprocessing)
- **real ≈ user** → Single-threaded, CPU-bound work
- **real > user** → Program spent time waiting (I/O, sleep)

**Example with threading_demo.py:**
```bash
time python3 threading_demo.py
# real    0m4.1s    (4 seconds you waited)
# user    0m0.02s   (only 0.02s of actual CPU work!)
```

This shows threading_demo.py spent almost all time **waiting** (sleep), not calculating — perfect for threading!

**Try:**
- `time python3 threading_demo.py`  → Notice real > user (I/O wait)
- `time python3 cpu_demo.py`         → Notice user > real (multiple cores)

### 2. cProfile — Where is Time Spent?

**cProfile** shows which functions take the most time in your code.

**Works best on single-process scripts** (multiprocessing can cause issues):

```bash
# Profile threading_demo.py and show output
python3 -m cProfile -s cumulative threading_demo.py
```

**Understanding the output:**
```
   ncalls  tottime  percall  cumtime  filename:lineno(function)
        3    3.001    1.000    3.001  {built-in method time.sleep}
        1    0.000    0.000    3.005  threading_demo.py:10(fetch_data)
```

| Column | Meaning |
|--------|---------|
| `ncalls` | How many times the function was called |
| `tottime` | Total time spent in the function (seconds) |
| `percall` | Average time per call |
| `cumtime` | Time in function + all functions it called |
| `filename:lineno(function)` | Where the function is defined |

**Key insight:** `time.sleep` took 3 seconds — that's the I/O wait! This proves threading helps with I/O.

**Save and analyze later:**
```bash
# Save profile to file
python3 -m cProfile -o stats.prof threading_demo.py

# View top 10 functions
python3 -c "import pstats; p = pstats.Stats('stats.prof'); p.sort_stats('cumulative').print_stats(10)"
```

**Note:** cProfile + multiprocessing has issues on macOS. For cpu_demo.py, use simple `time` command instead.

### 3. Line Profiler — Line by Line

```bash
pip install line_profiler
```

Add to your code:
```python
from line_profiler import LineProfiler

profiler = LineProfiler()

@profiler
def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

slow_function()
profiler.print_stats()
```

---

## Chapter 7: Real Debugging Scenario

### Problem: Server is Slow

```bash
# Step 1: What's using CPU?
ps aux --sort=-%cpu | head -10

# Step 2: How many threads?
pidstat -t -p <SLOW_PID>

# Step 3: What files is it accessing?
lsof -p <SLOW_PID>

# Step 4: Check memory
ps aux --sort=-%mem | head -10

# Step 5: Profile the Python code
python3 -m cProfile -s cumulative -m uvicorn main:app
```

### Common Issues:

| Symptom | Likely Cause | Check With |
|---------|--------------|------------|
| High CPU, low throughput | CPU-bound task | `pidstat`, profiler |
| High memory, growing | Memory leak | `ps aux`, memory_profiler |
| Slow responses, low CPU | I/O bottleneck | `iostat`, `lsof` |
| Many processes | Too many workers | `ps aux \| grep <app>` |

---

## Quick Reference

```bash
# Processes
ps aux | grep python          # Find Python processes
top -p <PID>                  # Watch specific process
kill -9 <PID>                 # Force kill process

# Threads
pidstat -t -p <PID>           # Watch threads
nproc                         # Number of CPU cores

# Network
lsof -i :8000                 # What's on port 8000?
netstat -tlnp                 # All listening ports

# Performance
ab -n 1000 -c 10 <url>        # Load test
wrk -t12 -c400 -d30s <url>    # Better load test
time <command>                # Time a command
```

---

## Summary

- **Process** = Isolated, heavy, good for CPU work
- **Thread** = Shared memory, light, good for I/O work
- **Python GIL** = Use multiprocessing for CPU, threading for I/O
- **WSGI** (Flask/Django) = Multiple processes, 1 request per worker
- **ASGI** (FastAPI) = Fewer processes, many requests per worker (async)
- **Linux tools** = `ps`, `top`, `pidstat`, `lsof` for monitoring
- **Load testing** = `ab`, `wrk`, `locust` for benchmarking
