from src.utils.http_request import http_request


def test_valid_request() -> None:
    """Test the `http_request` function with a valid URL.

    Assert:
        The function should return a response object because the URL is valid.
    """
    assert http_request("https://google.com") is not None


def test_invalid_request() -> None:
    """Test the `http_request` function with an invalid URL.

    Assert:
        The function should return None because the URL is invalid.
    """
    assert http_request("https://elgoog.com") is None
