"""
Threading demo: Good for I/O-bound tasks (network, disk)
Run: python3 threading_demo.py
"""
import threading
import time

def fetch_data(url):
    """Simulate HTTP request (I/O wait)"""
    time.sleep(1)  # 1 second network delay
    return f"Data from {url}"

urls = ["http://api1.com", "http://api2.com", "http://api3.com"]

# Sequential version
print("=== Sequential (1 at a time) ===")
start = time.time()
for url in urls:
    result = fetch_data(url)
    print(f"Got: {result}")
print(f"Total time: {time.time() - start:.1f}s")  # ~3 seconds

print()

# Threaded version
print("=== Threading (all at once) ===")
start = time.time()
threads = []
results = []

def fetch_and_store(url):
    results.append(fetch_data(url))

for url in urls:
    t = threading.Thread(target=fetch_and_store, args=(url,))
    t.start()
    threads.append(t)

# Wait for all to finish
for t in threads:
    t.join()

print(f"Results: {results}")
print(f"Total time: {time.time() - start:.1f}s")  # ~1 second!
print("\nThreads are great for I/O-bound tasks like HTTP requests!")

# =============================================================================
# CHALLENGE: Modify This Script
# =============================================================================
#
# CHALLENGE 1: Add more URLs
#   Add 2 more URLs to the list (urls = ["...", "...", "...", "...", "..."])
#   Run again and see it still takes ~1 second (threading scales!)
#
# CHALLENGE 2: Change the sleep time
#   Change time.sleep(1) to time.sleep(2)
#   Sequential would take 6s, threading still takes 2s
#
# CHALLENGE 3: Use a real HTTP request
#   Replace time.sleep(1) with:
#       import requests
#       return requests.get(url).text
#   Then test with real URLs like:
#       urls = ["https://httpbin.org/get", "https://httpbin.org/delay/1"]
#
# HINT: For challenge 3, you need to install requests first:
#   pip install requests
