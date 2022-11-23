from pytest_mock import MockerFixture
from requests.models import Response

from aswe.utils.request import http_request


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
