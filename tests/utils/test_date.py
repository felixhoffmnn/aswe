import datetime

from aswe.utils.date import get_next_saturday, validate_date


def test_get_next_saturday() -> None:
    """Test `get_next_saturday` method for workdays of a fixed week."""

    assert get_next_saturday().weekday() == 5

    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    days_diff = (get_next_saturday() - today).days

    match today.weekday():
        case 0:
            assert days_diff == 5
        case 1:
            assert days_diff == 4
        case 2:
            assert days_diff == 3
        case 3:
            assert days_diff == 2
        case 4:
            assert days_diff == 1
        case 5:
            assert days_diff == 0
        case 6:
            assert days_diff == 6


def test_valid_date() -> None:
    """Test the `validate_date` function with a valid date."""
    assert validate_date("2020-02-02") is True
    assert validate_date("2022-30-01") is False
    assert validate_date("2022-09-09T22:00:00Z") is True
    assert validate_date("2022-09-01Ttest") is False
