from datetime import datetime, timedelta

from vvspy import get_trips

from aswe.api.navigation.trip_data import Connection, Trip


def get_latest_connection(start_station: str, end_station: str, arrival_time: datetime) -> Trip | None:
    """Provides a trip from the start location to the end location before a deadline

    Args:
        start_station (str): VVS-id for starting station
        end_station (str): VVS-id for end station
        arrival_time (datetime): Latest possible time for arrival

    Returns:
        Trip | None: An object containing all the information about the trip
    """
    trips = get_trips(start_station, end_station, check_time=arrival_time, limit=10)

    trip_output = None
    for trip in reversed(trips):
        if trip.connections[-1].destination.arrival_time_estimated < arrival_time:
            connections = []
            for connection in trip.connections:
                connections.append(
                    Connection(
                        train_name=connection.transportation.disassembled_name,
                        start_location=connection.origin.name,
                        start_time=connection.origin.departure_time_estimated,
                        end_location=connection.destination.name,
                        end_time=connection.destination.arrival_time_estimated,
                    )
                )
            trip_duration = (
                trip.connections[-1].destination.arrival_time_estimated
                - trip.connections[0].origin.departure_time_estimated
            ).total_seconds()
            trip_output = Trip(duration=int(trip_duration / 60), connections=connections)
            break
    return trip_output


def get_next_connection(start_station: str, end_station: str) -> Trip | None:
    """Provides the next trip from the start location to the end location

    Args:
        start_station (str): VVS-id for starting station
        end_station (str): VVS-id for end station

    Returns:
        Trip | None: An object containing all the information about the trip
    """
    trips = get_trips(start_station, end_station, limit=10)

    trip_output = None
    for trip in trips:
        if trip.connections[0].origin.departure_time_estimated + timedelta(hours=1) > datetime.now():
            connections = []
            for connection in trip.connections:
                connections.append(
                    Connection(
                        train_name=connection.transportation.disassembled_name,
                        start_location=connection.origin.name,
                        start_time=connection.origin.departure_time_estimated + timedelta(hours=1),
                        end_location=connection.destination.name,
                        end_time=connection.destination.arrival_time_estimated + timedelta(hours=1),
                    )
                )
            trip_duration = (
                trip.connections[-1].destination.arrival_time_estimated
                - trip.connections[0].origin.departure_time_estimated
            ).total_seconds()
            trip_output = Trip(duration=int(trip_duration / 60), connections=connections)
            break

    return trip_output
