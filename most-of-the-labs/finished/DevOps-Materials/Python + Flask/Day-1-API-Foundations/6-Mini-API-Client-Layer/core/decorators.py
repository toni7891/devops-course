import functools
import time
import requests


def handle_errors(func):
    """
    Decorator לטיפול בשגיאות רשת ו-API.
    עוטף כל פונקציה ומחזיר מבנה אחיד במקרה של כישלון.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection failed"}
        except requests.exceptions.JSONDecodeError:
            return {"success": False, "error": "Response was not valid JSON"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    return wrapper


def log_execution(func):
    """
    Decorator שמתעד כל קריאה לפונקציה: שם, זמן ריצה, תוצאה.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] → {func.__name__}() called")
        start = time.time()

        result = func(*args, **kwargs)

        elapsed = time.time() - start
        success = isinstance(result, dict) and result.get("success", False)
        status_str = "SUCCESS" if success else "FAILED"
        print(f"[LOG] ← {func.__name__}() | {status_str} | {elapsed:.3f}s")

        return result
    return wrapper
