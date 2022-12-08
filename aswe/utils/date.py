from datetime import datetime, timedelta

from loguru import logger


def get_next_saturday() -> datetime:
    """Get next Saturday relative to today.
    Returns Saturday of current week if today is either a working day or Saturday.
    Returns next week's Saturday if today is a Sunday.

    Returns
    -------
    datetime.datetime
        Next Saturday
    """
    today = datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    delta_to_next_saturday = (5 - today.weekday()) % 7
    next_saturday = today + timedelta(days=delta_to_next_saturday)

    return next_saturday


def check_timedelta(last_trigger: datetime, delta: int) -> bool:
    """Calculate the time difference between the last trigger and the current time.
    If the time difference is greater than the given delta, return `True`, else `False`.

    Parameters
    ----------
    last_trigger : datetime
        The last time when the proactivity was triggered
    delta : int
        The interval in minutes

    Returns
    -------
    bool
        If the time difference is greater than the given delta, return `True`, else `False`
    """
    current_time = datetime.now()

    if current_time - last_trigger > timedelta(minutes=delta):
        return True

    return False


def validate_date(date: str, include_time: bool | None = None) -> bool:
    """Validates Time format for either `YYYY-MM-DD` or `YYYY-MM-DDThh:mm:ss`

    Parameters
    ----------
    date : str
        Date as type string that should be checked
    include_time : bool | None, optional
        Whether date should include time. If None methods tries finding correct type. _By default `None`._

    Returns
    -------
    bool:
        Whether date is valid.
    """
    if ("T" in date and include_time is None) or include_time is True:
        try:
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            logger.error(f"Incorrect date format, required: `YYYY-MM-DDThh:mm:ssZ`, given: {date}")
            return False
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Incorrect date format, required: `YYYY-MM-DD`, given: {date}")
            return False

    return True
