from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class MapsTrip:
    """Dataclass supposed to store the data of a connection retrieved from google maps

    Attributes
    ----------
    duration : int
        Duration in minutes
    distance : int
        Distance in meters
    """

    duration: int
    distance: int


class MapsTripMode(str, Enum):
    """Enum for google maps api trip modes"""

    BICYCLING = "bicycling"
    DRIVING = "driving"
    TRANSIT = "transit"
    WALKING = "walking"


@dataclass
class Connection:
    """Dataclass supposed to store the data of a single vvs connection

    Attributes
    ----------
    train_name : str
        Name of the train
    start_location : str
        Name of the starting location
    start_time : datetime
        Departure time of the train
    end_lcocation : str
        Name of the end location
    end_time : datetime
        Arrival time of the train
    """

    train_name: str
    start_location: str
    start_time: datetime
    end_location: str
    end_time: datetime


@dataclass
class Trip:
    """Dataclass supposed to store the data of a vvs trip

    Attributes
    ----------
    duration : int
        Time needed for the entire trip in minutes
    connections : list[Connection]
        All connections that are part of the trip
    """

    duration: int
    connections: list[Connection]
