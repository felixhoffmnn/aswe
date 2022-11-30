import datetime

from aswe.utils.general import get_next_saturday


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
