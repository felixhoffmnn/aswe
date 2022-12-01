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
