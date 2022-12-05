from datetime import datetime, timedelta


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
