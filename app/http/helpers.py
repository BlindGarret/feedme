from functools import wraps
from time import sleep

from requests.exceptions import HTTPError


def retry_http_429(f, max_retries=5):
    """
    Decorator to retry a function when it raises a HTTP 429 status code.

    :param f: Function to decorate.
    :param max_retries: Maximum number of retries.
    :return: Decorated function.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        for _ in range(max_retries):
            try:
                return f(*args, **kwargs)
            except HTTPError as e:
                if e.response.status_code == 429:
                    retry_after = e.response.headers.get("Retry-After")
                    if retry_after is not None:
                        sleep(int(retry_after) if retry_after.isdigit() else 0)
                        continue
                raise

    return wrapper
