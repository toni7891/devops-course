import functools
import time

from flask import jsonify, make_response, request


def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] → {func.__name__}()")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[LOG] ← {func.__name__}() | {elapsed:.3f}s")
        return result
    return wrapper


def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"success": False, "error": {"message": str(e), "code": 500}}), 500
    return wrapper


def validate_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.json:
            return jsonify({"success": False, "error": {"message": "JSON body required", "code": 400}}), 400
        return func(*args, **kwargs)
    return wrapper


# BONUS: adds X-Response-Time header to the response
def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        elapsed_ms = (time.time() - start) * 1000

        # rv may be a Response or a (Response, status) tuple
        response = make_response(rv)
        response.headers["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
        return response
    return wrapper
