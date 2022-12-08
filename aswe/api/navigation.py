import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

import googlemaps as gmaps
from loguru import logger
from requests import Response
from vvspy import get_trips

_GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


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


def get_latest_connection(start_station: str, end_station: str, arrival_time: datetime) -> Trip | None:
    """Provides a trip from the start location to the end location before a deadline

    Parameters
    ----------
    start_station : str
        VVS-id for starting station
    end_station : str
        VVS-id for end station
    arrival_time : datetime
        Latest possible time for arrival

    Returns
    -------
    Trip | None
        An object containing all the information about the trip
    """
    trips = get_trips(start_station, end_station, check_time=arrival_time, limit=10)

    if isinstance(trips, Response):
        logger.error("Got unexpected response from VVS API")
        return None

    if trips is None or len(trips) == 0:
        logger.error("No trips found")
        return None

    last_trip = trips[-1]

    if last_trip.connections[-1].destination.arrival_time_estimated < arrival_time:
        connections = [
            Connection(
                train_name=connection.transportation.disassembled_name,
                start_location=connection.origin.name,
                start_time=connection.origin.departure_time_estimated,
                end_location=connection.destination.name,
                end_time=connection.destination.arrival_time_estimated,
            )
            for connection in last_trip.connections
        ]
        trip_duration = (
            last_trip.connections[-1].destination.arrival_time_estimated
            - last_trip.connections[0].origin.departure_time_estimated
        ).total_seconds()
        trip_output = Trip(duration=int(trip_duration / 60), connections=connections)
        return trip_output

    return None


def get_next_connection(start_station: str, end_station: str) -> Trip | None:
    """Provides the next trip from the start location to the end location

    Parameters
    ----------
    start_station : str
        VVS-id for starting station
    end_station : str
        VVS-id for end station

    Returns
    -------
    Trip | None
        An object containing all the information about the trip
    """
    trips = get_trips(start_station, end_station, limit=10)

    if isinstance(trips, Response):
        logger.error("Got unexpected response from VVS API")
        return None

    if trips is None or len(trips) == 0:
        logger.error("No trips found")
        return None

    next_trip = trips[0]

    if next_trip.connections[0].origin.departure_time_estimated + timedelta(hours=1) > datetime.now():
        connections = [
            Connection(
                train_name=connection.transportation.disassembled_name,
                start_location=connection.origin.name,
                start_time=connection.origin.departure_time_estimated + timedelta(hours=1),
                end_location=connection.destination.name,
                end_time=connection.destination.arrival_time_estimated + timedelta(hours=1),
            )
            for connection in next_trip.connections
        ]
        trip_duration = (
            next_trip.connections[-1].destination.arrival_time_estimated
            - next_trip.connections[0].origin.departure_time_estimated
        ).total_seconds()
        trip_output = Trip(duration=int(trip_duration / 60), connections=connections)
        return trip_output

    return None


def get_maps_connection(start_location: str, end_location: str, mode: MapsTripMode) -> MapsTrip:
    """Provides the distance and duration for a trip with a specific transportation type

    Parameters
    ----------
    start_location : str
        Name of the location the trip starts
    end_location : str
        Name of the location the trip ends
    mode : MapsTripMode
        Type of transportation. Possible values: 'driving', 'walking', 'bicycling' or 'transit'

    Returns
    -------
    MapsTrip
        A MapsTrip object containing the distance and duration of the trip
    """
    client = gmaps.Client(key=_GOOGLE_MAPS_API_KEY)
    directions_result = client.directions(start_location, end_location, mode=mode.value)  # type: ignore

    distance = int(directions_result[0]["legs"][0]["distance"]["value"])
    duration = int(directions_result[0]["legs"][0]["duration"]["value"] / 60)

    logger.debug(f"Maps: From {start_location} to {end_location} with {mode}: {distance} meter, {duration} minutes")

    return MapsTrip(
        distance=distance,
        duration=duration,
    )
