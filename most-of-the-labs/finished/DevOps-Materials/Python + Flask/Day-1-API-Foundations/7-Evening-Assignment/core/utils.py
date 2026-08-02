def build_response(success, data=None, error=None):
    if success:
        return {"success": True, "data": data}
    return {"success": False, "error": error or "Unknown error"}


def check_status(response, expected=200):
    if response.status_code != expected:
        return build_response(
            success=False,
            error=f"Expected status {expected}, got {response.status_code}"
        )
    return None
