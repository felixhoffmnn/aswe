from aswe.utils.validate import validate_date


def test_valid_date() -> None:
    """Test the `validate_date` function with a valid date."""
    assert validate_date("2020-02-02") is True


def test_invalid_date() -> None:
    """Test the ``validate_date function with an invalid date"""
    assert validate_date("2022-30-01") is False


def test_valid_datetime() -> None:
    """Test the ``validate_date function with an valid datetime"""
    assert validate_date("2022-09-09T22:00:00") is True


def test_invalid_datetime() -> None:
    """Test the ``validate_date function with an invalid datetime"""
    assert validate_date("2022-09-01Ttest") is False
