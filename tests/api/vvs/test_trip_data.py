from datetime import datetime

import pytest

from aswe.api.navigation.trip_data import Connection, Trip


def test_connection_required_fields() -> None:
    """Test required fields for `Connection` dataclass"""
    with pytest.raises(TypeError):
        Connection()  # pylint: disable=no-value-for-parameter


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
        Trip()  # pylint: disable=no-value-for-parameter


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
