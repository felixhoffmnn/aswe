from datetime import datetime, timedelta

from aswe.api.navigation.trip_data import Connection
from aswe.api.navigation.vvs import get_latest_connection, get_next_connection


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
