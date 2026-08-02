def build_response(success, data=None, error=None):
    """
    בונה מבנה תשובה אחיד לכל הפונקציות.

    Args:
        success: האם הפעולה הצליחה
        data: הנתונים שהוחזרו (אם הצליחה)
        error: תיאור השגיאה (אם נכשלה)

    Returns:
        dict: {"success": bool, "data": ...} או {"success": False, "error": "..."}
    """
    if success:
        return {"success": True, "data": data}
    return {"success": False, "error": error or "Unknown error"}


def check_status(response, expected=200):
    """
    בודק שה-status code תואם למצופה.

    Returns:
        None אם הכל תקין
        dict שגיאה אם לא
    """
    if response.status_code != expected:
        return build_response(
            success=False,
            error=f"Expected status {expected}, got {response.status_code}"
        )
    return None
