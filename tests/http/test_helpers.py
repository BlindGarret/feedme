# type: ignore[reportFunctionMemberAccess]

from pytest import mark
from requests import Response
from requests.exceptions import HTTPError

from app.http.helpers import retry_http_429

http_429_resp = Response()
http_429_resp.status_code = 429
http_429_resp.headers = {
    "Retry-After": "0",
}
http_429 = HTTPError(response=http_429_resp)


def retry_func(ret_vals):
    instance = ret_vals[retry_func.calls]
    print(instance)
    retry_func.calls += 1
    if isinstance(instance, Exception):
        raise instance
    return instance


@mark.parametrize(
    "max_retries,expected,returns",
    [
        (
            3,
            3,
            [
                http_429,
                http_429,
                http_429,
                http_429,
                http_429,
            ],
        ),
        (
            5,
            5,
            [
                http_429,
                http_429,
                http_429,
                http_429,
                http_429,
            ],
        ),
        (
            5,
            4,
            [
                http_429,
                http_429,
                http_429,
                None,
            ],
        ),
        (
            5,
            1,
            [
                None,
            ],
        ),
        (
            5,
            1,
            [Exception("non matching exception")],
        ),
    ],
)
def test_retry_http_429_call_count_is_expected(max_retries, expected, returns):
    retry_func.calls = 0
    fn = retry_http_429(retry_func, max_retries=max_retries)

    try:
        fn(returns)
    except Exception:
        pass

    assert retry_func.calls == expected
