import datetime
import os
from sys import platform


def clear_shell() -> None:
    """Clears any previous text in the shell"""
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


def get_next_saturday() -> datetime.datetime:
    """Get next Saturday relative to today.\n
    Returns Saturay of current week if today is either a working day or Saturday.\n
    Returns next week's Saturday if today is a Sunday.


    Returns
    -------
    datetime.datetime
        Next Saturday
    """
    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    delta_to_next_saturday = (5 - today.weekday()) % 7
    next_saturday = today + datetime.timedelta(days=delta_to_next_saturday)

    return next_saturday
