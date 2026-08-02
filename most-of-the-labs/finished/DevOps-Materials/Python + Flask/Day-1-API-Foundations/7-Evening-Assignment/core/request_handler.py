import requests
from core.decorators import handle_errors, log_execution
from core.utils import build_response, check_status

BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_TIMEOUT = 5


@log_execution
@handle_errors
def make_request(url, method="GET", params=None, body=None):
    response = requests.request(
        method=method.upper(),
        url=url,
        params=params,
        json=body,
        timeout=DEFAULT_TIMEOUT
    )

    status_error = check_status(response)
    if status_error:
        return status_error

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return build_response(success=False, error="Response is not valid JSON")

    return build_response(success=True, data=data)
