# ? Disable private attribute access to test class methods
# pylint: disable=redefined-outer-name,protected-access

from requests.models import Response

from aswe.utils.validate import validate_api, validate_date


def test_valid_date() -> None:
    """Test the `validate_date` function with a valid date."""
    assert validate_date("2020-02-02") is True


def test_invalid_date() -> None:
    """Test the `validate_date` function with an invalid date"""
    assert validate_date("2022-30-01") is False


def test_valid_datetime() -> None:
    """Test the `validate_date` function with an valid datetime"""
    assert validate_date("2022-09-09T22:00:00Z") is True


def test_invalid_datetime() -> None:
    """Test the `validate_date` function with an invalid datetime"""
    assert validate_date("2022-09-01Ttest") is False


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
