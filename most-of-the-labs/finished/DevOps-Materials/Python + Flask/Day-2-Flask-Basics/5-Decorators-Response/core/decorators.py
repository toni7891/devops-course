import functools
import time

from flask import jsonify, request


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
            return jsonify({"success": False, "error": str(e)}), 500
    return wrapper


def validate_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.json:
            return jsonify({"success": False, "error": "JSON body required"}), 400
        return func(*args, **kwargs)
    return wrapper
