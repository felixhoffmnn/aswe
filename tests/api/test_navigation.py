# pylint: disable=no-value-for-parameter
from datetime import datetime, timedelta

import pytest

from aswe.api.navigation import (
    Connection,
    MapsTrip,
    MapsTripMode,
    Trip,
    get_latest_connection,
    get_maps_connection,
    get_next_connection,
)


def test_get_latest_connection() -> None:
    """Test `aswe.api.navigation.vvs.get_latest_connection`"""
    trip = get_latest_connection("de:08111:6056", "de:08111:355", datetime.now() + timedelta(hours=2))

    if trip is not None:
        assert isinstance(trip.duration, int)
        assert isinstance(trip.connections, list)
        if len(trip.connections) > 0:
            assert isinstance(trip.connections[0], Connection)


def test_get_next_connection() -> None:
    """Test `aswe.api.navigation.vvs.get_next_connection`"""
    trip = get_next_connection("de:08111:6056", "de:08111:355")

    if trip is not None:
        assert isinstance(trip.duration, int)
        assert isinstance(trip.connections, list)
        if len(trip.connections) > 0:
            assert isinstance(trip.connections[0], Connection)


def test_get_maps_connection() -> None:
    """Test `aswe.api.navigation.maps.get_maps_connection`"""
    maps_trip = get_maps_connection("Ernsthaldenstraße 43", "Rotebühlplatz 41", MapsTripMode.DRIVING)

    assert isinstance(maps_trip.duration, int)
    assert isinstance(maps_trip.distance, int)


def test_maps_trip_required_fields() -> None:
    """Test required fields for `MapsTrip` dataclass"""
    with pytest.raises(TypeError):
        MapsTrip()  # type: ignore


def test_maps_trip_variable_types() -> None:
    """Test variable types for `MapsTrip` dataclass"""
    maps_trip = MapsTrip(distance=1000, duration=60)

    assert isinstance(maps_trip.distance, int)
    assert isinstance(maps_trip.duration, int)


def test_connection_required_fields() -> None:
    """Test required fields for `Connection` dataclass"""
    with pytest.raises(TypeError):
        Connection()  # type: ignore


def test_connection_variable_types() -> None:
    """Test variable types for `Connection` dataclass"""
    connection = Connection(
        train_name="S1",
        start_location="Stadtmitte",
        start_time=datetime.now(),
        end_location="Hauptbahnhof",
        end_time=datetime.now(),
    )

    assert isinstance(connection.train_name, str)
    assert isinstance(connection.start_location, str)
    assert isinstance(connection.start_time, datetime)
    assert isinstance(connection.end_location, str)
    assert isinstance(connection.end_time, datetime)


def test_trip_required_fields() -> None:
    """Test required fields for `Trip` dataclass"""
    with pytest.raises(TypeError):
        Trip()  # type: ignore


def test_trip_variable_types() -> None:
    """Test variable types for `Trip` dataclass"""
    trip = Trip(
        duration=20,
        connections=[
            Connection(
                train_name="S1",
                start_location="Stadtmitte",
                start_time=datetime.now(),
                end_location="Hauptbahnhof",
                end_time=datetime.now(),
            )
        ],
    )

    assert isinstance(trip.duration, int)
    assert isinstance(trip.connections, list)
    assert isinstance(trip.connections[0], Connection)
