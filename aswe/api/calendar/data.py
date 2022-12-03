from dataclasses import dataclass


@dataclass
class Event:
    """Dataclass storing Event data

    Parameters
    ----------
    title : str
        The title of the event
    description : str
        The description of the event
    location : str
        The location the event takes place
    full_day : bool
        Stores if the event is active the entire day
    date : str
        The date of a full-day event with the format "yyyy-MM-dd"
    start_time : str
        The start time of a non-full-day event with the format "yyyy-MM-ddTHH:mm:ss+01:00"
    end_time : str
        The end time of a non-full-day event with the format "yyyy-MM-ddTHH:mm:ss+01:00"
    """

    title: str
    """The title of the event"""

    description: str
    """The description of the event"""

    location: str
    """The location the event takes place"""

    full_day: bool
    """Stores if the event is active the entire day"""

    date: str
    """The date of a full-day event with the format "yyyy-MM-dd"""

    start_time: str
    """The start time of a non-full-day event with the format "yyyy-MM-ddTHH:mm:ss+01:00"""

    end_time: str
    """The end time of a non-full-day event with the format "yyyy-MM-ddTHH:mm:ss+01:00"""
