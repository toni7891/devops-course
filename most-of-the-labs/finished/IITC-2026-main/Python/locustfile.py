"""
Locust load test configuration.
Run with: locust -f locustfile.py
Then open http://localhost:8089 in browser
"""
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
        self.client.get("/admin/")

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


# =============================================================================
# CHALLENGE: Modify This Load Test
# =============================================================================
#
# CHALLENGE 1: Add more endpoints
#   Add a @task to test POST /students for Flask and Django too
#   Example for FlaskUser:
#       @task
#       def create_student(self):
#           self.client.post("/students", json={"name": "Test", "email": "test@test.com"})
#
# CHALLENGE 2: Change the wait time
#   Make users more aggressive by changing wait_time to between(0.1, 0.5)
#   Or make them slower with between(5, 10)
#   Watch how the server responds differently
#
# CHALLENGE 3: Add randomness
#   Import random and make request weights random:
#       import random
#       @task(random.randint(1, 5))
#       def get_students(self):
#           ...
#
# CHALLENGE 4: Test only one framework at a time
#   Comment out 2 of the 3 user classes to focus on just one
#   Compare results between FlaskUser, DjangoUser, and FastAPIUser
