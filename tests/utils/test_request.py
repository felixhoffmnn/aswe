from pytest_mock import MockerFixture
from requests.models import Response

from aswe.utils.request import http_request, validate_api


def test_valid_request() -> None:
    """Test the `http_request` function with a valid URL"""
    assert http_request("https://google.com") is not None


def test_invalid_request() -> None:
    """Test the `http_request` function with an invalid URL"""
    assert http_request("https://elgoog.com") is None


def test_exception(mocker: MockerFixture) -> None:
    """Test the `http_request` function with invalid status code from response"""

    # * HTTPError
    mock_response = Response()
    mock_response.status_code = 401
    mocker.patch("aswe.utils.request.requests.get", return_value=mock_response)

    assert http_request("lorem") is None

    # * Other Exception
    mock_response = Response()
    mock_response.status_code = 202
    mocker.patch("aswe.utils.request.requests.get", return_value=mock_response)

    assert http_request("lorem") is None


def test_valid_api_response() -> None:
    """Test `validate_api` function"""

    key_error_response = Response()
    key_error_response._content = b"{}"

    assert validate_api(key_error_response) is False

    limit_not_reached = Response()
    limit_not_reached._content = b'{"errors": {"requests": ""}}'

    assert validate_api(limit_not_reached) is False

    limit_reached = Response()
    limit_reached._content = b'{"errors": {"requests": "You have reached the request limit for the day"}}'

    assert validate_api(limit_reached) is True
